# F1-VSS 0 - Shared context (run first)

**Purpose:** context for the F1 / Formula E demos: the rules, conventions and known pitfalls each demo follows. It builds nothing.

---

## Paste into Cursor

```
Prompt ID: f1-vss/00-shared-context

Context for every F1 / Formula E demo. This prompt builds nothing: it sets the rules each demo prompt follows. Follow .cursor/rules/build-day.mdc and use the matching skill in .cursor/skills/ for every platform call. Do not invent your own storage layer, endpoints or model hosts.

What already exists (do not rebuild it):
- Two races, f1-academy_race and formula-e_race, ingested and indexed (about the first 15 minutes of each broadcast): segmented, captioned, embedded, YOLO detections stored. Check with retrieval-videos (explore) and retrieval-dashboard.
- Re-ingest with ingest-reingest-videos (max 3 chunks and 30 seconds per request, so one chunk in practice). Uploading new video is disabled.
- Search: retrieval-search. Grounded Q&A: retrieval-agent-qa. Playback and detections: retrieval-videos.
- The models run inside the VSS pipeline; reach them only through the skills.
- Tables: vast-database-vastdb-read and vast-database-vastdb-write, in schema f1demo.

Conventions
- Python: python3 -m venv .venv. If it fails with "ensurepip is not available", use python3 -m venv --without-pip .venv, then get-pip.py.
- One race: search with metadata_filters {"camera_id": ...} (formula_e_broadcast-1, f1_academy_broadcast-1). Explore returns 100 chunks per call, so page with offset and filter by file name.
- race_id = the file name between the YYYYMMDD_HHMMSS_ prefix and _chunk_NNNN. Race time = chunk_index x 30 + offset (nominal).
- Clips: play the 5 s segment clips from search results through a small server-side proxy in your app. Never show playback_url in the UI; it carries a token.
- Run the app on the VM on its own port.

Rules for every demo
- Each demo builds its own app, with whatever setup it needs. Show every result in the app, not in files.
- Do not deploy DataEngine functions or polling loops; run on the footage that is already indexed.
- When done, show the single best clip first.
- If stuck, use ask-cosmos.
```
