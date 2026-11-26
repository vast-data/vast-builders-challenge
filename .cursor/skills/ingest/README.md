# Ingest (vss2)

> **Build on the footage that is already indexed.** Re-ingest is not available on this
> stack: the backend has no re-ingest route. Upload works but is not recommended, because
> it uses GPUs every team shares; the upload skill keeps it to one short clip at a time.

## Skills

| Skill | Mechanism | Purpose |
|-------|-----------|---------|
| [upload-video](upload-video/SKILL.md) | `upload_clip.py` → `POST /api/v1/videos/upload` | Not recommended. Cut and upload one short clip (30 s or less) with its own camera label, one at a time |

Auth is a backend JWT from `POST /api/v1/auth/login`.
Team URL and credentials come only from the single `/config/*.config` file on
the VM. Skills must not search the repository's `team-configs/`.
