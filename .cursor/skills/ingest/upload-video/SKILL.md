---
name: ingest-upload-video
description: >-
  Not recommended: uploads run on GPUs every team shares. Uploads one short clip (30 s or
  less) of the user's own footage with upload_clip.py. Use only when the user asks to add
  footage that is not in the archive.
---

> **Not recommended.** Uploading works, but every uploaded second is captioned, embedded
> and scanned for objects on GPUs shared by every team. Build on the footage that is
> already indexed where you can. When the user does need their own footage, keep it to a
> short clip and use the script below.

# Ingest: upload a short clip (vss2)

## Before uploading, ask the user

1. Which video file.
2. The start and end time of the part to upload (30 s or less).
3. Optionally, a prompt that says what the captions should describe.
4. Confirmation. Say once that uploads use GPU time shared by every team.

## Defaults, and what the user can change

| | Default | If the user asks for more |
|---|---|---|
| Clip length | 30 s | `--yes` |
| One at a time | an upload waits for the one before it | nothing to change |
| Team allowance | 10 uploads or 5 minutes of video in total | the script asks to confirm; run again with `--yes` |
| Camera label | `team-upload` | fixed |

## Run it

See [vast-database/README.md](../../vast-database/README.md#prerequisites-python--vastdb)
for Python setup and resolve `$PY` first. `ffmpeg` must be on the VM. The script reads
the team config from `/config/<team>.config`.

```bash
PY=~/vastdb-venv/bin/python; [ -x "$PY" ] || PY=python3
UP=.cursor/skills/ingest/upload-video/upload_clip.py

"$PY" $UP upload /path/to/video.mp4 --start 12 --end 32 \
  --prompt "Describe what the players are doing, in one short sentence."
"$PY" $UP status                       # this team's uploads, and anything still in progress
"$PY" $UP remove "s3://<bucket>/<key>"  # the original_video printed after an upload
```

## What the script does

1. **Cuts the part you named** and uploads only that, never the whole file.
2. **Gives the clip its own camera label.** Uploaded clips stay out of the F1 and football
   results, and a search limited to that label is fast because it covers only those clips.
3. **Takes one upload at a time.** If an earlier upload is still being processed, it says
   so and waits for it before sending the next one.
4. **Waits until the clip is searchable,** then prints its `original_video`, how to search
   it and how to remove it.

Exit codes: `0` done, `2` a default was exceeded and nothing was uploaded (read the
message; ask the user), `3` still being processed after the wait (check `status` later).

## After the upload

Search the clip with its label:

```json
{"camera_id": "team-upload"}
```

Removing an upload deletes its file, its clips and its records. Only the uploader can
remove it.

## Agent instructions

1. Do not suggest uploading. Use this skill only when the user asks to add their own footage.
2. Ask for the file, the start and end time, and confirmation.
3. Run `upload_clip.py`; do not call the upload route yourself and do not loop over a folder.
4. If the script exits with `2`, tell the user what it said and ask before running again
   with `--yes`.
5. Report the `original_video` it prints, and how to search and remove the clip.
6. Never print credentials or the bearer token.
