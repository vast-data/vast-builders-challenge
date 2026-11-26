# DFL 0 - Context (run first)

**Purpose:** context for the DFL demo: the rules, conventions and known pitfalls it follows. It builds no app; it runs one setup step.

---

## Paste into Cursor

```
Prompt ID: dfl-archive/00-foundation

Context for the Bundesliga (DFL) demo. This prompt builds no app: it runs one setup step and sets the rules the demo prompt follows. Follow .cursor/rules/build-day.mdc and use the matching skill in .cursor/skills/ for every platform call. Do not invent your own storage layer, endpoints or model hosts.

Setup (once per stack, before any demo)
- Run the era setup with vast-database-football-eras: `label_eras.py status`, then `label_eras.py apply` if the eras are not applied yet. Tell me in one line what it did.

What already exists (do not rebuild it):
- More than 30 full Bundesliga matches (about 100 minutes each, 1970-71 to 2026-27) are ingested and indexed: segmented, captioned, embedded, YOLO detections stored. Listed by retrieval-videos (explore).
- Build on the footage and captions that are already indexed: no re-ingest, and upload only if I ask (ingest-upload-video).
- Search: retrieval-search. Playback and detections: retrieval-videos.
- The models run inside the VSS pipeline; reach them only through the skills.
- Tables: vast-database-vastdb-read and vast-database-vastdb-write, in schema dfl.

Conventions
- Python on the VM: use the system python3 if `python3 -c "import vastdb"` works. Only if it fails, follow the Python setup in .cursor/skills/vast-database/README.md. The deployed app does not use a venv; it installs from requirements.txt.
- Each match is stored as 30 s chunks, each its own original_video. Do not list the archive unless the demo needs every chunk: search results already carry each hit's file name, time and clip source.
- Per-segment captions, sources and times are in each chunk's `chunks[].timeline[]` (retrieval-videos explore), one entry per 5 s segment. A chunk's top-level `reasoning_content` is only the first segment's caption — read `timeline[]` for every segment.
- File names read <upload date>_<upload time>_<season>_<competition>_<home>-vs-<away>_chunk_<NNNN> (a segment clip adds _segment_<SS>_of_<TT>), for example 20261107_162225_1970-71_bundesliga_bayern-munchen-vs-1-fc-koln_chunk_0000.mp4. match_id = <season>_<competition>_<home>-vs-<away>. Split on "_": competition and team names contain hyphens. Match time = NNNN x 30 + the hit's segment_start_sec. File names carry no match date, so leave match_date as an editable placeholder.
- Search filters are camera_id, capture_type, location and object_classes, one value each. Every match shares camera_id bundesliga-01; after the era setup, location holds the clip's era (germany-1970-84, germany-1985-97, germany-2000-09, germany-2010-16, germany-2017-26). Season, competition and team are not filters: take them from the file name in your own code.
- Search one era by default, with metadata_filters {"camera_id": "bundesliga-01", "location": "<era>"}. Give the app an era control: the most recent era (germany-2017-26) is selected at first, the user can add eras or choose "All eras", and a short note says that more eras make a search take longer. For two eras, run one search per era and merge the hits by similarity_score. For three or more, or "All eras", run one search with camera_id only and top_k 100 and keep the hits whose season is in the selected eras. If an era search has no good hits, say so and offer the other eras; do not widen the search silently.
- retrieval-search can take several seconds per query. If the app does not show the summary, send system_prompt "Reply with only the word OK." and ignore llm_synthesis. While a search runs, show the results layout as a loading skeleton with a short neutral status line ("Searching the archive..."), and show a clear message if it fails or returns nothing. Never display how long a search took or will take.
- Clips: play the 5 s segment clips from search results through a small server-side proxy in your app. Never show playback_url in the UI; it carries a token. Do not cut clips with ffmpeg.
- Deploy the app with deploy-app-no-registry (it runs on the cluster at `/app/`; if the team already has an app deployed, give this one its own name and the path `/app/<name>/`); a quick local run on the VM is fine for testing before you deploy.

Licensing rules (the demo seeds these)
- Use types: social, broadcast, documentary, advertising.
- Territory groups: DACH (DE, AT, CH, LI, LU) and ROW. Partner: Sportcast for DACH, IMG for ROW.
- Rights: one row per asset x territory group x use type. The only ungranted combination is ROW advertising. Each rights row carries an example term (for example "12 months"), marked as a demo value.
- usage_events territory is the buyer's country. Rate card unit types: query, clip, minute. Example rates are demo values.

UI rules for every demo
- Layout: a ranked list on the left and one player panel on the right. Selecting a row plays it there. Filter chips with hit counts sit above the list.
- Cards: match, time as M:SS and score (2 decimals) on one line. Caption trimmed to its first sentence (about 90 characters, ending in "..."), expandable. Drop the "The video shows" lead-in. Never repeat the season or competition inside its group.
- Load a clip only when it is played, and show one player at a time (each 5 s clip is about 3 MB).
- Counts read "N hits". Keep only hits with similarity_score at or above a cutoff, default 0.35, and let the user change it in the app (a slider is fine). Show a clear "no good hits" state instead of weak results.
- Suggested searches: show a row of 3 to 4 buttons labelled "Suggested searches", using the queries the demo prompt lists. Clicking one runs that search right away and shows its results, as if it had been typed. Keep the free-text search box as well.

Rules for every demo
- Each demo builds its own app, with whatever setup it needs. Show every result in the app, not in files.
- When you finish, tell me in chat which suggested search and which result to play first as the best example. The app itself does not run a search or load a clip until the user asks for one.
- If I ask you to mock the responses for rapid UI iteration: save one real search response, whole, return it in place of live searches, and show a note on the page, "Using mock search results". When I say the UI work is done, remove the mock and the note and run one live search to confirm.
- If stuck, use ask-help.
```
