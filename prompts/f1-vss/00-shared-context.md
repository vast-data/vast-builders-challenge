# F1-VSS 0 - Shared context (run first)

**Purpose:** context for the F1 / Formula E demos: the rules, conventions and known pitfalls each demo follows. It builds nothing.

---

## Paste into Cursor

```
Prompt ID: f1-vss/00-shared-context

Context for every F1 / Formula E demo. This prompt builds nothing: it sets the rules each demo prompt follows. Follow .cursor/rules/build-day.mdc and use the matching skill in .cursor/skills/ for every platform call. Do not invent your own storage layer, endpoints or model hosts.

What already exists (do not rebuild it):
- Two races, f1-academy_race (92 chunks, about 46 minutes) and formula-e_race (101 chunks, about 50 minutes), ingested and indexed: segmented, captioned, embedded, YOLO detections stored. Check with retrieval-videos (explore) and retrieval-dashboard.
- Re-ingest with ingest-reingest-videos (max 3 chunks and 30 seconds per request, so one chunk in practice). Uploading new video is disabled.
- Search: retrieval-search. Grounded Q&A: retrieval-agent-qa. Playback and detections: retrieval-videos.
- The models run inside the VSS pipeline; reach them only through the skills.
- Tables: vast-database-vastdb-read and vast-database-vastdb-write, in schema f1demo.

Conventions
- Python: python3 -m venv .venv. If it fails with "ensurepip is not available", use python3 -m venv --without-pip .venv, then get-pip.py.
- F1 footage: filter search with metadata_filters {"camera_id": "f1-01"}. That value covers both races, so keep only the hits for the race you want by file name: original_video / source contains f1-academy_race or formula-e_race.
- To list a race's chunks, call explore with location=england (returns the F1 chunks only, 100 per call, so two pages with offset), then filter by file name the same way.
- Per-segment captions, sources and times are in each chunk's `chunks[].timeline[]` (retrieval-videos explore), one entry per 5 s segment. A chunk's top-level `reasoning_content` is only the first segment's caption — read `timeline[]` for every segment.
- A wrong camera_id returns zero results with no error, so check values with /metadata/values when a filtered search comes back empty.
- race_id = the file name between the YYYYMMDD_HHMMSS_ prefix and _chunk_NNNN. Race time = chunk_index x 30 + offset (nominal).
- Clips: play the 5 s segment clips from search results through a small server-side proxy in your app. Never show playback_url in the UI; it carries a token.
- Deploy the app with deployment-deploy-app-no-registry (it runs on the cluster at `/app`); a quick local run on the VM is fine for testing before you deploy.

UI rules for every demo
- Layout: a ranked list on the left and one player panel on the right. Selecting a row plays it there. Filter chips with hit counts sit above the list.
- Cards: race, time as M:SS and score (2 decimals) on one line. Caption trimmed to its first sentence (about 90 characters, ending in "..."), expandable. Drop the "The video shows" lead-in. Never repeat the race inside its group.
- Load a clip only when it is played, and show one player at a time (each 5 s clip is about 4.6 MB).
- Counts read "N hits". Show a clear "no good hits" state instead of weak results.
- Suggested searches: show a row of 3 to 4 buttons labelled "Suggested searches", using the queries the demo prompt lists. Clicking one runs that search right away and shows its results, as if it had been typed. Keep the free-text search box as well.

Rules for every demo
- Each demo builds its own app, with whatever setup it needs. Show every result in the app, not in files.
- Do not deploy DataEngine functions or polling loops; run on the footage that is already indexed.
- When done, show the single best clip first.
- If stuck, use ask-cosmos.
```
