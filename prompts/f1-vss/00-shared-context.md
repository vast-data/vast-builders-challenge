# F1-VSS 0 - Shared context and scaffold (run first)

**Purpose:** common helpers (clip playback) that the F1 / Formula E demos use. Segmentation, captioning, embedding and detection are already handled by the running VSS pipeline.

---

## Paste into Cursor

```
Prompt ID: f1-vss/00-shared-context

You are building demos on the VSS stack that is already running in this workspace. Follow .cursor/rules/build-day.mdc and use the matching skill in .cursor/skills/ for every platform call. Do not invent your own storage layer, endpoints or model hosts.

What already exists (do not rebuild it):
- Race footage (F1 Academy / Formula E MP4s) is ingested and indexed: segmented, captioned by Cosmos3-Reason, embedded with Cosmos-Embed1 (256-dim), YOLO11 detections stored. race_id = the part of the file name between the YYYYMMDD_HHMMSS_ prefix and _chunk_NNNN (e.g. formula-e_race). Footage is indexed as 30 s chunks of 5 s segments; race time = chunk_index x 30 + offset. Check with retrieval-videos (explore) and retrieval-dashboard.
- Re-run a race with a demo-specific prompt: ingest-reingest-videos (max 3 chunks and 30 seconds per request). Uploading new video is disabled.
- Search: retrieval-search. Grounded Q&A: retrieval-agent-qa. Playback, per-video summary, detections: retrieval-videos. Auth: retrieval-login.
- Models (Cosmos3-Reason VLM/LLM, YOLO11, Cosmos-Embed1) run inside the VSS pipeline. You reach them only through the skills above; do not call model endpoints directly.
- Raw VAST DataBase access for our own tables: vast-database-vastdb-read (reads) and vast-database-vastdb-write (create schema or table, insert). Put demo tables in schema f1demo.

Step 0: scaffold before any demo
1. Repo layout: common/, demos/<demo_name>/, config/.
2. Clips: use the retrieval-videos skill to play the segment clips that search results already return (the `source` field, 5 s each). For a longer moment, play consecutive segments back to back in the app. Do not cut or store clips yourself unless a demo's output is an edited video.
3. Each demo gets its own folder with a README and an app entry point (app.py) that runs it on one race. Do not deploy DataEngine functions or polling loops; run on the footage that is already indexed.

Rules for every demo
- Show every result in the app, not in files. Each clip shown includes: asset_id, start_ts, end_ts, playback_url.
- Build a small web UI for each demo that shows its results and plays the clips (segment clips via retrieval-videos). Run it on the VM, or host it with the deploy-app-no-registry skill.
- When done, show the single best clip first in the app.
- If stuck, use ask-cosmos.
```
