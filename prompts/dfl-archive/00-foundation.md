# DFL 0 - Context (run first)

**Purpose:** context for the DFL demo: the rules, conventions and known pitfalls it follows. It builds nothing.

---

## Paste into Cursor

```
Prompt ID: dfl-archive/00-foundation

Context for the Bundesliga (DFL) demo. This prompt builds nothing: it sets the rules the demo prompt follows. Follow .cursor/rules/build-day.mdc and use the matching skill in .cursor/skills/ for every platform call. Do not write raw REST or invent endpoints.

What already exists (do not rebuild it):
- Five Bundesliga matches (about 15 minutes each) are ingested and indexed: segmented, captioned, embedded, YOLO detections stored. Check with retrieval-videos (explore) and retrieval-dashboard.
- Re-ingest with ingest-reingest-videos (max 3 chunks and 30 seconds per request, so one chunk in practice). Uploading new video is disabled.
- Search: retrieval-search. Playback and detections: retrieval-videos.
- The models run inside the VSS pipeline; reach them only through the skills.
- Tables: vast-database-vastdb-read and vast-database-vastdb-write, in schema dfl.

Conventions
- Python: python3 -m venv .venv. If it fails with "ensurepip is not available", use python3 -m venv --without-pip .venv, then get-pip.py.
- Each match is stored as 30 s chunks, each its own original_video. Explore returns 100 chunks per call, so page with offset and filter by file name.
- match_id = the file name slug <season>_<competition>_<home>-vs-<away> (not the leading timestamp, which is the upload time). Match time = chunk_index x 30 + offset. File names carry no match date, so leave match_date as an editable placeholder.
- Native search filters are only camera_id, capture_type, location and object_classes, one value each. camera_id identifies one match. Filter season, competition and team in your own code from the file name.
- retrieval-search takes about 3 s per query (it always adds an LLM summary): show a spinner.
- Clips: play the 5 s segment clips from search results through a small server-side proxy in your app. Never show playback_url in the UI; it carries a token. Do not cut clips with ffmpeg.
- Run the app on the VM on its own port.

Licensing rules (the demo seeds these)
- Use types: social, broadcast, documentary, advertising.
- Territory groups: DACH (DE, AT, CH, LI, LU) and ROW. Partner: Sportcast for DACH, IMG for ROW.
- Rights: one row per asset x territory group x use type. The only ungranted combination is ROW advertising.
- usage_events territory is the buyer's country. Rate card unit types: query, clip, minute. Example rates are demo values.

Rules for every demo
- Each demo builds its own app, with whatever setup it needs. Show every result in the app, not in files.
- When done, show the single best clip first.
- If stuck, use ask-cosmos.
```
