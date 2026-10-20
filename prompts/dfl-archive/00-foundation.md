# DFL 0 - Foundation (run first)

**Purpose:** shared tables, usage meter and Streamlit app shell that the DFL storefront demo (prompt 3) builds on. The footage is already indexed (segmented, captioned, embedded, YOLO-detected) by the existing VSS pipeline, so this prompt only adds the DFL-specific business layer on top.

---

## Paste into Cursor

```
Prompt ID: dfl-archive/00-foundation

Build the shared foundation for the Bundesliga (DFL) licensing demo on top of the stack that is already running. Follow .cursor/rules/build-day.mdc. Use the matching skill in .cursor/skills/ for every platform call; do not write raw REST or invent endpoints.

What already exists (do not rebuild it):
- The DFL footage is already ingested and indexed by the VSS pipeline: segmented, captioned by Cosmos3-Reason, embedded with Cosmos-Embed1, YOLO detections stored. Use retrieval-videos (explore) to confirm, and retrieval-dashboard for ingest health.
- To re-run a video with a DFL-specific prompt, use ingest-reingest-videos (max 3 chunks and 30 seconds per request). Uploading new video is disabled.
- Search, playback and summaries come from retrieval-search, retrieval-videos and retrieval-agent-qa. Log in with retrieval-login.

Build these pieces:

1. Asset metadata
   - At startup the app lists the indexed chunks with retrieval-videos (explore) and parses season, competition, home and away from the file names. The names carry no match date, so show an editable table in the app where match_date can be filled in (placeholder within the season, marked unverified).
   - Save it to a VAST DataBase table assets with one row per chunk: asset_id = <match>_c<NNNN>, plus match_id, chunk_index, match_offset_s, original_video, season, match_date, home, away, competition, duration_s, era, source. Join to the indexed archive on original_video. era = decade bucket from match_date (1960s, 1970s, ...). The index stores each match as 30 s chunks, each its own original_video. Group chunks by the filename slug (<season>_<competition>_<home>-vs-<away>), not the leading timestamp, which is the upload time.
   - Use retrieval-list-metadata to see the native filters: only camera_id, capture_type, location and object_classes, one value each. camera_id identifies one match, so push single-match filters as camera_id, and filter season, competition and team through the assets table instead.

2. Business tables (VAST DataBase, schema dfl; read with vast-database-vastdb-read, create tables and insert rows with vast-database-vastdb-write)
   - rights(asset_id, territory, use_type, term_months, partner, rate_ref): one row per asset x territory group (DACH, ROW) x use_type. territory holds the group. partner = Sportcast for DACH (DE, AT, CH, LI, LU), IMG elsewhere. Leave at least one combination ungranted so demo 3 can show a blocked case.
   - rate_card(rate_ref, use_type, unit_type, territory, price_eur): unit_type is one of query, clip, minute.
   - usage_events(event_id, ts, buyer_id, action, asset_id, start_s, end_s, units, unit_type, territory, use_type, partner, gpu_seconds, model, price_eur)
   - In usage_events, territory is the buyer's country.

3. Meter
   - meter.py with a decorator @metered(action, unit_type) that wraps any search, render, export or dataset call, records elapsed GPU-backed time, looks up price in rate_card, resolves partner from rights, and inserts one usage_events row.
   - Every user-facing action in every demo goes through it.

4. App shell
   - One Streamlit app, app.py (install streamlit if it is missing). Sidebar picks the buyer persona (id, territory, use type). Tabs: Matches (the editable assets table), Storefront, Meter.
   - Meter tab: live usage_events totals by buyer, action and partner, plus the latest 50 rows.
   - Shared helpers:
     - search_text(query, filters, k) via retrieval-search. It takes about 3 s per query (it always adds an LLM summary), so show a spinner and do not promise sub-second results.
     - play_clip(original_video, start_s, end_s): play the matching segment clips (5 s each) in the app with retrieval-videos, back to back for a longer moment. Do not cut clips with ffmpeg.

5. Seed data
   - rate_card with example rates (search per query, clip retrieved, licensed minute by use type), clearly marked as demo values.
   - A default rights row per territory group for every asset, leaving one combination ungranted.

Acceptance: assets is populated for every indexed match; search_text returns hits with timecodes; one search writes one usage_events row; README.md explains setup and run. If anything is stuck, use ask-cosmos.
```
