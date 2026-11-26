#!/usr/bin/env python3
"""Upload a short clip into this team's VSS archive, one at a time.

Modes:
  upload FILE --start S --end E   cut, upload and wait until searchable
  status                          this team's uploads: clips indexed, and anything still in progress
  remove ORIGINAL_VIDEO           delete one of this team's uploads (file, clips and records)
"""

from __future__ import annotations

import argparse
import datetime as dt
import math
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

LABEL = "team-upload"          # camera_id given to every uploaded clip
MAX_SECONDS = 30               # default longest clip; --yes lifts it
ALLOW_UPLOADS = 10             # past this many uploads (or ALLOW_SECONDS of video) the script asks for --yes
ALLOW_SECONDS = 300
WAIT_MINUTES = 10              # longest wait for an earlier upload, and for the new clip to be searchable
RECENT_MINUTES = 15            # an upload older than this that never finished is treated as stuck, not in progress
CLIP_SECONDS = 5               # the pipeline cuts every upload into clips of this length
KEY_TIME = re.compile(r"/(\d{8}_\d{6})_")


def _team_config() -> Path:
    configs = sorted(Path("/config").glob("*.config"))
    if len(configs) != 1:
        print(f"Expected exactly one /config/*.config team file; found {len(configs)}", file=sys.stderr)
        sys.exit(1)
    return configs[0]


def load_env(path: Path) -> dict[str, str]:
    env: dict[str, str] = {}
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        env[key.strip()] = value.strip().strip('"').strip("'")
    return env


def with_scheme(url: str) -> str:
    return url if url.startswith(("http://", "https://")) else f"http://{url}"


class Stack:
    """Everything the script asks the stack: the backend API, the chunk storage, and the search table."""

    def __init__(self, env: dict[str, str]):
        import requests

        self.env = env
        self.http = requests.Session()
        self.base = with_scheme(env["INGRESS_URL"]).rstrip("/")
        r = self.http.post(self.base + "/api/v1/auth/login", json={"username": env["USERNAME"], "password": env["PASSWORD"]}, timeout=60)
        r.raise_for_status()
        self.http.headers["Authorization"] = "Bearer " + r.json()["access_token"]
        self._s3 = None
        self._db = None

    # ---- backend API
    def max_upload_mb(self) -> float:
        return float(self.http.get(self.base + "/api/v1/config", timeout=30).json()["app"]["max_upload_size_mb"])

    def fully_indexed(self) -> set[str]:
        """original_video of this user's uploads that explore lists, i.e. that are fully indexed."""
        r = self.http.get(self.base + "/api/v1/videos/explore", params={"scope": "mine", "limit": 100, "offset": 0}, timeout=120)
        r.raise_for_status()
        return {c.get("original_video") for c in r.json().get("chunks", [])}

    def upload(self, clip: str, fields: dict[str, str]) -> dict:
        with open(clip, "rb") as fh:
            r = self.http.post(self.base + "/api/v1/videos/upload", files={"file": (os.path.basename(clip), fh, "video/mp4")}, data=fields, timeout=300)
        if r.status_code != 200:
            raise RuntimeError(f"upload refused: HTTP {r.status_code} {r.text[:200]}")
        return r.json()

    def remove(self, original_video: str) -> dict:
        r = self.http.delete(self.base + "/api/v1/videos", params={"original_video": original_video}, timeout=300)
        if r.status_code != 200:
            raise RuntimeError(f"delete refused: HTTP {r.status_code} {r.text[:200]}")
        return r.json()

    # ---- chunk storage (what has been received)
    def recent_chunks(self) -> list[str]:
        """original_video of chunks this team uploaded in the last RECENT_MINUTES, newest last."""
        if self._s3 is None:
            import boto3

            env = self.env
            self._s3 = boto3.client("s3", endpoint_url=with_scheme(env["S3_ENDPOINT"]), aws_access_key_id=env["ACCESS_KEY"],
                                    aws_secret_access_key=env["SECRET_KEY"], verify=False)
        env = self.env
        now = dt.datetime.now(dt.timezone.utc)
        out = []
        for day in {now.strftime("%Y%m%d"), (now - dt.timedelta(minutes=RECENT_MINUTES)).strftime("%Y%m%d")}:
            resp = self._s3.list_objects_v2(Bucket=env["S3_CHUNKS_BUCKET"], Prefix=f"{env['USERNAME']}/{day}_")
            for obj in resp.get("Contents", []):
                m = KEY_TIME.search("/" + obj["Key"].split("/", 1)[-1])
                if not m:
                    continue
                when = dt.datetime.strptime(m.group(1), "%Y%m%d_%H%M%S").replace(tzinfo=dt.timezone.utc)
                if (now - when).total_seconds() <= RECENT_MINUTES * 60:
                    out.append((when, f"s3://{env['S3_CHUNKS_BUCKET']}/{obj['Key']}"))
        return [uri for _when, uri in sorted(out)]

    # ---- search table (what has been indexed)
    def clips_by_upload(self, label: str) -> dict[str, int]:
        """Clips in the index per original_video, for rows carrying the upload label."""
        if self._db is None:
            import vastdb

            env = self.env
            self._db = vastdb.connect(endpoint=with_scheme(env["S3_ENDPOINT"]), access=env["ACCESS_KEY"], secret=env["SECRET_KEY"], ssl_verify=False)
        env = self.env
        with self._db.transaction() as tx:
            t = tx.bucket(env["VASTDB_BUCKET"]).schema(env.get("VDB_SCHEMA", "vss-schema")).table(env.get("VDB_COLLECTION", "vss-collection"))
            videos = t.select(columns=["original_video"], predicate=(t["camera_id"] == label)).read_all().column("original_video").to_pylist()
        counts: dict[str, int] = {}
        for v in videos:
            counts[v] = counts.get(v, 0) + 1
        return counts


def in_progress(stack: Stack, done: set[str] | None = None) -> list[str]:
    """Uploads received in the last few minutes that are not fully indexed yet."""
    recent = stack.recent_chunks()
    if not recent:
        return []
    if done is None:
        done = stack.fully_indexed()
    return [uri for uri in recent if uri not in done]


def wait_for_turn(stack: Stack, timeout_s: int) -> bool:
    busy = in_progress(stack)
    if not busy:
        return True
    print(f"An earlier upload is still being processed ({len(busy)} in progress). Yours will start when it finishes.", flush=True)
    end = time.time() + timeout_s
    while time.time() < end:
        time.sleep(5)
        if not in_progress(stack):
            return True
    return False


def cut(source: str, start: float, end: float, out: str) -> None:
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(start), "-t", str(end - start), "-i", source,
                    "-c:v", "libx264", "-preset", "veryfast", "-c:a", "aac", out], check=True)


def cmd_upload(args, stack: Stack) -> int:
    if not os.path.isfile(args.file):
        print(f"No such file: {args.file}", file=sys.stderr)
        return 1
    seconds = args.end - args.start
    if seconds <= 0:
        print("--end must be after --start", file=sys.stderr)
        return 1
    if seconds > MAX_SECONDS and not args.yes:
        print(f"That is {seconds:.0f} s. Uploads are processed on GPUs shared by every team, so the default limit is "
              f"{MAX_SECONDS} s. Pick a shorter start and end, or pass --yes if the user asked for the longer clip.")
        return 2

    used = stack.clips_by_upload(LABEL)
    used_seconds = sum(used.values()) * CLIP_SECONDS
    if (len(used) >= ALLOW_UPLOADS or used_seconds + seconds > ALLOW_SECONDS) and not args.yes:
        print(f"This team has already uploaded {len(used)} clip(s), about {used_seconds} s of video. Uploads use GPU time "
              f"shared by every team. Confirm with the user, then run again with --yes.")
        return 2

    with tempfile.TemporaryDirectory(prefix="vss-upload-") as tmp:
        clip = os.path.join(tmp, Path(args.file).stem[:40] + ".mp4")
        cut(args.file, args.start, args.end, clip)
        size_mb = os.path.getsize(clip) / 1e6
        limit_mb = stack.max_upload_mb()
        if size_mb > limit_mb:
            print(f"The cut clip is {size_mb:.0f} MB and the backend accepts at most {limit_mb:.0f} MB. Pick a shorter part.")
            return 2

        if not wait_for_turn(stack, WAIT_MINUTES * 60):
            print(f"The earlier upload is still being processed after {WAIT_MINUTES} min. Nothing was uploaded; run this again later.")
            return 3

        fields = {"is_public": "false", "camera_id": LABEL, "capture_type": "general"}
        if args.prompt:
            fields["custom_prompt"] = args.prompt[:800]
        up = stack.upload(clip, fields)

    keys = up.get("object_keys") or [up.get("object_key")]
    uris = [f"s3://{stack.env['S3_CHUNKS_BUCKET']}/{k}" for k in keys if k]
    expected = math.ceil(seconds / CLIP_SECONDS)
    print(f"Uploaded {seconds:.0f} s as {len(uris)} chunk(s). Waiting until it is searchable (about {expected} clips)...", flush=True)
    end = time.time() + WAIT_MINUTES * 60
    indexed = 0
    while time.time() < end:
        time.sleep(5)
        by_upload = stack.clips_by_upload(LABEL)
        indexed = sum(by_upload.get(u, 0) for u in uris)
        if indexed >= expected and all(u in stack.fully_indexed() for u in uris):
            break
    else:
        print(f"Still being processed after {WAIT_MINUTES} min: {indexed} of about {expected} clips indexed. Check later with: status")
        for u in uris:
            print("original_video:", u)
        return 3
    print(f"Searchable: {indexed} clips.")
    for u in uris:
        print("original_video:", u)
    print(f'Search it with metadata_filters {{"camera_id": "{LABEL}"}}.')
    print("Remove it with: upload_clip.py remove <original_video>")
    return 0


def cmd_status(args, stack: Stack) -> int:
    by_upload = stack.clips_by_upload(LABEL)
    done = stack.fully_indexed()
    busy = in_progress(stack, done)   # one reading of the stack for both lists, so they agree
    print(f"uploads with camera_id {LABEL}: {len(by_upload)}, about {sum(by_upload.values()) * CLIP_SECONDS} s of video")
    for uri, n in sorted(by_upload.items()):
        print(f"  {n} clips | {'searchable' if uri in done else 'being processed'} | {uri}")
    print(f"in progress now: {len(busy)}")
    for uri in busy:
        print("  being processed |", uri)
    return 0


def cmd_remove(args, stack: Stack) -> int:
    res = stack.remove(args.original_video)
    print(f"removed: {res.get('segments_deleted', 0)} clips, {res.get('objects_deleted', 0)} stored objects")
    if res.get("object_errors"):
        print("some objects could not be removed:", str(res["object_errors"])[:200])
        return 1
    return 0


def main() -> None:
    p = argparse.ArgumentParser(description="Upload a short clip into the team's VSS archive, one at a time")
    sub = p.add_subparsers(dest="mode", required=True)
    up = sub.add_parser("upload")
    up.add_argument("file")
    up.add_argument("--start", type=float, required=True, help="start time in seconds")
    up.add_argument("--end", type=float, required=True, help="end time in seconds")
    up.add_argument("--prompt", help="custom caption prompt (max 800 characters)")
    up.add_argument("--yes", action="store_true", help=f"the user confirmed more than {MAX_SECONDS} s, or going past the team's upload allowance")
    st = sub.add_parser("status")
    rm = sub.add_parser("remove")
    rm.add_argument("original_video", help="the s3:// URI printed after the upload")
    args = p.parse_args()

    override = os.environ.get("VAST_ENV_FILE")
    env = load_env(Path(override) if override else _team_config())
    missing = [k for k in ("INGRESS_URL", "USERNAME", "PASSWORD", "S3_ENDPOINT", "ACCESS_KEY", "SECRET_KEY", "S3_CHUNKS_BUCKET", "VASTDB_BUCKET") if not env.get(k)]
    if missing:
        print("Missing in the team config: " + ", ".join(missing), file=sys.stderr)
        sys.exit(1)
    stack = Stack(env)
    sys.exit({"upload": cmd_upload, "status": cmd_status, "remove": cmd_remove}[args.mode](args, stack))


if __name__ == "__main__":
    main()
