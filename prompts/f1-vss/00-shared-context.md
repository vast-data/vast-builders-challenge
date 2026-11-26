# F1-VSS 0 - Shared context (run first)

**Purpose:** context for the F1 / Formula E demos: the rules, conventions and known pitfalls each demo follows. It builds nothing.

---

## Paste into Cursor

```
Prompt ID: f1-vss/00-shared-context

Context for every F1 / Formula E demo. This prompt builds nothing: it sets the rules each demo prompt follows. Follow .cursor/rules/build-day.mdc and use the matching skill in .cursor/skills/ for every platform call. Do not invent your own storage layer, endpoints or model hosts.

What already exists (do not rebuild it):
- Two races, f1-academy_race (about 46 minutes) and formula-e_race (about 50 minutes), ingested and indexed: segmented, captioned, embedded, YOLO detections stored. Listed by retrieval-videos (explore).
- Build on the footage and captions that are already indexed: no re-ingest, and upload only if I ask (ingest-upload-video).
- Search: retrieval-search. Grounded Q&A: retrieval-agent-qa. Playback and detections: retrieval-videos.
- The models run inside the VSS pipeline; reach them only through the skills.
- Tables: vast-database-vastdb-read and vast-database-vastdb-write, in schema f1demo.

Conventions
- Python on the VM: use the system python3 if `python3 -c "import vastdb"` works. Only if it fails, follow the Python setup in .cursor/skills/vast-database/README.md. The deployed app does not use a venv; it installs from requirements.txt.
- F1 footage: filter search with metadata_filters {"camera_id": "f1-01"}. That value covers both races, so keep only the hits for the race you want by file name: original_video / source contains f1-academy_race or formula-e_race.
- To list a race's chunks, call explore with location=england (returns the F1 chunks only, 100 per call, so page with offset until a page comes back short), then filter by file name the same way. List once and reuse the result; do not call explore on every page view.
- Per-segment captions, sources and times are in each chunk's `chunks[].timeline[]` (retrieval-videos explore), one entry per 5 s segment. A chunk's top-level `reasoning_content` is only the first segment's caption — read `timeline[]` for every segment.
- A wrong camera_id returns zero results with no error, so check values with /metadata/values when a filtered search comes back empty.
- race_id = the file name between the YYYYMMDD_HHMMSS_ prefix and _chunk_NNNN. Race time = chunk_index x 30 + offset (nominal).
- retrieval-search can take several seconds per query. If the app does not show the summary, send system_prompt "Reply with only the word OK." and ignore llm_synthesis. While a search runs, show the results layout as a loading skeleton with a short neutral status line ("Searching the races..."), and show a clear message if it fails or returns nothing. Never display how long a search took or will take.
- Clips: play the 5 s segment clips from search results through a small server-side proxy in your app. Never show playback_url in the UI; it carries a token.
- Deploy the app with deploy-app-no-registry (it runs on the cluster at `/app/`; if the team already has an app deployed, give this one its own name and the path `/app/<name>/`); a quick local run on the VM is fine for testing before you deploy.

UI rules for every demo
- Layout: a ranked list on the left and one player panel on the right. Selecting a row plays it there. Filter chips with hit counts sit above the list.
- Cards: race, time as M:SS and score (2 decimals) on one line. Caption trimmed to its first sentence (about 90 characters, ending in "..."), expandable. Drop the "The video shows" lead-in. Never repeat the race inside its group.
- Load a clip only when it is played, and show one player at a time (each 5 s clip is about 6 MB).
- Counts read "N hits". For search results shown to the user, keep only hits with similarity_score at or above a cutoff, default 0.30, and let the user change it in the app (a slider is fine), unless the demo prompt selects hits another way. Show a clear "no good hits" state instead of weak results.
- Suggested searches: show a row of 3 to 4 buttons labelled "Suggested searches", using the queries the demo prompt lists. Clicking one runs that search right away and shows its results, as if it had been typed. Keep the free-text search box as well.

Rules for every demo
- Each demo builds its own app, with whatever setup it needs. Show every result in the app, not in files.
- Do not deploy DataEngine functions or polling loops; run on the footage that is already indexed.
- When you finish, tell me in chat which suggested search and which result to play first as the best example. The app itself does not run a search or load a clip until the user asks for one.
- If I ask you to mock the responses for rapid UI iteration: save one real search response, whole, return it in place of live searches, and show a note on the page, "Using mock search results". When I say the UI work is done, remove the mock and the note and run one live search to confirm.
- If stuck, use ask-help.
```
