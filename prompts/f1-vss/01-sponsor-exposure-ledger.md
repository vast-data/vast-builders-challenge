# F1-VSS 1 - Sponsor exposure ledger

**Purpose:** measure on-screen seconds per sponsor in a race and show a best clip per brand.

Requires: `00-shared-context.md`.

---

## Paste into Cursor

```
Prompt ID: f1-vss/01-sponsor-exposure-ledger

Demo 1: sponsor exposure ledger.
Follow the F1 context prompt (f1-vss/00-shared-context) and build your own small app, including explore, search and the clip proxy.

The race is already captioned and indexed, and the models are reachable only through the pipeline. Measure exposure from the indexed captions and search results, not from per-frame model calls.

Steps
1. Brands: read the captions of one race (retrieval-videos explore, reasoning_content), list the sponsor names that appear in them, and show the list in the app for me to edit before scanning.
2. Create table f1demo.sponsor_exposure (run_id, race_id, brand, interval_id, start_ts, end_ts, seconds, mean_score, max_score, source, start_chunk_index) with vast-database-vastdb-write. start_ts and end_ts are race seconds = chunk_index x 30 + offset.
3. Count exposure from captions, not search: for the selected race, keep every 5 s segment whose caption names the brand (case-insensitive — captions write "crypto.com" lowercase) and treat each as 5 s of exposure. (retrieval-search returns at most 100 hits and can't be scoped to one race, so it would undercount.) Separately, run one retrieval-search per brand for "<brand> logo" to rank clips: keep a hit only if it belongs to the selected race (by file name) and its caption names the brand; use its score for the best-clip choice in step 5 and for mean_score/max_score on segments that have a hit, leaving those columns null where they don't. Set `source` to show the count came from captions. Suggested searches: "Red Bull logo", "Crypto.com logo", "Hard Rock logo", "Nissan logo". Red Bull, Crypto.com and Hard Rock are named only in f1-academy_race captions, Nissan only in formula-e_race; say so when the selected race has none.
4. Merge consecutive matching segments of the same brand into intervals (gap under 5 s) and insert them into sponsor_exposure.
5. The app shows per brand: total seconds, intervals, and a best clip (from the caption-confirmed hits, the one with the most brand mentions across neighbouring segments, then the highest score; if a brand has caption matches but no search hit in the selected race, use its first caption-matched segment as the best clip instead — it has no score; played with retrieval-videos, with its caption beside it labelled "caption says: <brand>, check the video"). State the race scanned and that the resolution is 5 s segments.

Done when
- Total seconds per brand sum correctly from intervals.
- Spot check: the best clip for each brand visibly shows that brand.
- Total seconds per brand equal 5 s x the number of segments in that race whose caption names the brand.
```
