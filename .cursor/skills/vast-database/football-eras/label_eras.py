#!/usr/bin/env python3
"""Label each football clip in the search table with its era, so a search can be limited to one era.

Setup step for the Bundesliga track. It writes ONE field, `location`, and only on rows whose
camera_id is bundesliga-01. Nothing else in the search table is touched, and no clip is added
or removed.

Modes:
  status   read-only: show how the football clips are labelled now
  apply    give every football clip its era (safe to run again; rows already right are skipped)
  restore  put every football clip back to the original value, `germany` (kept for reference)
"""

from __future__ import annotations

import argparse
import collections
import os
import re
import sys
from pathlib import Path

CAMERA = "bundesliga-01"
ORIGINAL = "germany"
# (label, first season start-year, last season start-year). Whole seasons stay together.
ERAS = (
    ("germany-1970-84", 0, 1984),
    ("germany-1985-97", 1985, 1999),
    ("germany-2000-09", 2000, 2009),
    ("germany-2010-16", 2010, 2016),
    ("germany-2017-26", 2017, 9999),
)
ERA_LABELS = tuple(label for label, _first, _last in ERAS)
# file name: <upload date>_<upload time>_<season>_<competition>_<home>-vs-<away>_chunk_NNNN
SEASON = re.compile(r"/\d{8}_\d{6}_(\d{4})-\d{2}_")
BATCH = 4000


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


def normalize_endpoint(url: str) -> str:
    return url if url.startswith(("http://", "https://")) else f"http://{url}"


def era_for(original_video: str) -> str | None:
    m = SEASON.search(original_video or "")
    if not m:
        return None
    year = int(m.group(1))
    return next((label for label, first, last in ERAS if first <= year <= last), None)


class SearchTable:
    """The team's search table, reduced to the two things this script does: read labels, set labels."""

    def __init__(self, env: dict[str, str]):
        import vastdb

        self.env = env
        self.session = vastdb.connect(
            endpoint=normalize_endpoint(env["S3_ENDPOINT"]),
            access=env["ACCESS_KEY"],
            secret=env["SECRET_KEY"],
            ssl_verify=False,
        )

    def _table(self, tx):
        env = self.env
        return tx.bucket(env["VASTDB_BUCKET"]).schema(env.get("VDB_SCHEMA", "vss-schema")).table(
            env.get("VDB_COLLECTION", "vss-collection")
        )

    def read(self) -> list[tuple[int, str, str]]:
        """(row id, original_video, location) for every football clip."""
        with self.session.transaction() as tx:
            t = self._table(tx)
            tb = t.select(
                columns=["original_video", "location"],
                predicate=(t["camera_id"] == CAMERA),
                internal_row_id=True,
            ).read_all()
        return list(
            zip(tb.column("$row_id").to_pylist(), tb.column("original_video").to_pylist(), tb.column("location").to_pylist())
        )

    def set_location(self, row_ids: list[int], value: str) -> None:
        import pyarrow as pa

        for i in range(0, len(row_ids), BATCH):
            part = row_ids[i : i + BATCH]
            with self.session.transaction() as tx:
                t = self._table(tx)
                ltype = t.arrow_schema.field("location").type
                rows = pa.table({"$row_id": pa.array(part, pa.uint64()), "location": pa.array([value] * len(part), ltype)})
                t.update(rows, columns=["location"])  # only this one column is written


def counts(rows) -> dict[str, int]:
    return dict(sorted(collections.Counter(loc for _id, _video, loc in rows).items()))


def describe(rows) -> str:
    if not rows:
        return "no football clips found"
    c = counts(rows)
    if set(c) == {ORIGINAL}:
        return "not applied (every football clip says 'germany')"
    if all(loc == era_for(video) for _id, video, loc in rows):
        return "applied (every football clip carries its era)"
    if set(c) <= set(ERA_LABELS) | {ORIGINAL}:
        return "partly applied (run apply to finish)"
    return "unexpected values (see the counts above)"


def main() -> None:
    parser = argparse.ArgumentParser(description="Label football clips with their era in the `location` field")
    parser.add_argument("mode", choices=("status", "apply", "restore"))
    args = parser.parse_args()

    override = os.environ.get("VAST_ENV_FILE")
    env = load_env(Path(override) if override else _team_config())
    missing = [k for k in ("S3_ENDPOINT", "ACCESS_KEY", "SECRET_KEY", "VASTDB_BUCKET") if not env.get(k)]
    if missing:
        print("Missing in the team config: " + ", ".join(missing), file=sys.stderr)
        sys.exit(1)

    table = SearchTable(env)
    rows = table.read()
    print(f"football clips: {len(rows)}")
    print(f"location values now: {counts(rows)}")

    if args.mode == "status":
        print("eras: " + describe(rows))
        return

    unknown = sorted(set(counts(rows)) - set(ERA_LABELS) - {ORIGINAL})
    if unknown:
        print(f"Stopping: unexpected location values {unknown}. Nothing was changed.", file=sys.stderr)
        sys.exit(1)

    if args.mode == "apply":
        target = {}
        for row_id, video, _loc in rows:
            era = era_for(video)
            if era is None:
                print(f"Stopping: cannot read the season from a file name ending ...{str(video)[-50:]}. Nothing was changed.", file=sys.stderr)
                sys.exit(1)
            target[row_id] = era
        todo = collections.defaultdict(list)
        for row_id, _video, loc in rows:
            if loc != target[row_id]:
                todo[target[row_id]].append(row_id)
    else:  # restore
        target = {row_id: ORIGINAL for row_id, _video, _loc in rows}
        todo = {ORIGINAL: [row_id for row_id, _video, loc in rows if loc != ORIGINAL]}

    changed = sum(len(v) for v in todo.values())
    for label, row_ids in todo.items():
        if row_ids:
            table.set_location(row_ids, label)

    after = table.read()
    print(f"clips relabelled: {changed}")
    print(f"location values after: {counts(after)}")
    ok = len(after) == len(rows) and all(loc == target.get(row_id) for row_id, _video, loc in after)
    print("eras: " + describe(after))
    print("OK" if ok else "CHECK NEEDED: not every clip has the expected value; run the same command again")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
