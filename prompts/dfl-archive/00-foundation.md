# DFL 0 - Foundation (run first)

**Purpose:** shared tables, usage meter and Streamlit app shell that DFL prompts 1 to 5 build on. The footage is already indexed (segmented, captioned, embedded, YOLO-detected) by the existing VSS pipeline, so this prompt only adds the DFL-specific business layer on top.

---

## Paste into Cursor

```
Build the shared foundation for five Bundesliga (DFL) archive demos on top of the stack that is already running. Follow .cursor/rules/build-day.mdc. Use the matching skill in .cursor/skills/ for every platform call; do not write raw REST or invent endpoints.

What already exists (do not rebuild it):
- The DFL footage is already ingested and indexed by the VSS pipeline: segmented, captioned by Cosmos3-Reason, embedded with Cosmos-Embed1, YOLO detections stored. Use retrieval-videos (explore) to confirm, and retrieval-dashboard for ingest health.
- If I hand you a new MP4, use ingest-upload-video. To re-run a video with a DFL-specific prompt, use ingest-reingest-videos.
- Search, playback and summaries come from retrieval-search, retrieval-videos and retrieval-agent-qa. Log in with retrieval-login.

Build these pieces:

1. Asset metadata
   - A sidecar CSV per match: file, season, date, home, away, competition, source.
   - A VAST DataBase table assets(asset_id, original_video, season, match_date, home, away, competition, duration_s, era, source), joined to the indexed archive on original_video. era = decade bucket from match_date (1960s, 1970s, ...).
   - Use retrieval-list-metadata to see which metadata fields the index already has, and map season/competition/teams onto those where possible so search can filter natively.

2. Business tables (VAST DataBase, schema dfl; follow the VastDB connection pattern in retrieval-vastdb-read)
   - rights(asset_id, territory, use_type, term_months, partner, rate_ref). partner = Sportcast for DACH (DE, AT, CH, LI, LU), IMG elsewhere.
   - rate_card(rate_ref, use_type, unit_type, territory, price_eur)
   - usage_events(event_id, ts, buyer_id, action, asset_id, start_s, end_s, units, unit_type, territory, use_type, partner, gpu_seconds, model, price_eur)

3. Meter
   - meter.py with a decorator @metered(action, unit_type) that wraps any search, render, export or dataset call, records elapsed GPU-backed time, looks up price in rate_card, resolves partner from rights, and inserts one usage_events row.
   - Every user-facing action in every demo goes through it.

4. App shell
   - One Streamlit app, app.py. Sidebar picks the buyer persona (id, territory, use type). One tab per demo: Search, Market reels, Storefront, Sponsors, Datasets, Meter.
   - Meter tab: live usage_events totals by buyer, action and partner, plus the latest 50 rows.
   - Shared helpers: search_text(query, filters, k) via retrieval-search; search_clip(segment or uploaded clip, filters, k) using a Cosmos-Embed1 video embedding (see the gpu README); cut_clip(original_video, start_s, end_s) with ffmpeg from the playback URL in retrieval-videos.

5. Seed data
   - rate_card with example rates (search per query, clip retrieved, minute rendered, licensed minute by use type, brand-minute, dataset hour), clearly marked as demo values.
   - A default rights row per territory group for every asset.

Acceptance: assets is populated for every indexed match; search_text returns hits with timecodes; one search writes one usage_events row; README.md explains setup and run. If anything is stuck, use ask-cosmos.
```
