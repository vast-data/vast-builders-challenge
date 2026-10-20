# F1-VSS 1 - Sponsor exposure ledger

**Purpose:** measure on-screen seconds per sponsor in a race and show a best clip per brand.

Requires: `00-shared-context.md`.

---

## Paste into Cursor

```
Prompt ID: f1-vss/01-sponsor-exposure-ledger

Demo 1: sponsor exposure ledger.

The race is already captioned and indexed, and the models are reachable only through the pipeline. Measure exposure from the indexed captions and search results, not from per-frame model calls.

Steps
1. Brands: build the brand list from brand names in the indexed captions (retrieval-videos explore, reasoning_content) for one race.
2. Create table f1demo.sponsor_exposure (race_id, brand, interval_id, start_ts, end_ts, seconds, mean_score, source, start_chunk_index) with vast-database-vastdb-write. start_ts and end_ts are race seconds = chunk_index x 30 + offset.
3. For each brand, run retrieval-search for "<brand> logo" filtered to the race. Treat each matching 5 s segment as 5 s of exposure and use the search score as confidence. Drop weak matches; pick the cutoff by checking a few results.
4. Merge consecutive matching segments of the same brand into intervals (gap under 5 s) and insert them into sponsor_exposure.
5. The app shows per brand: total seconds, intervals, and a best clip (the highest-scoring segment, played with retrieval-videos). State the race scanned and that the resolution is 5 s segments.

Done when
- Total seconds per brand sum correctly from intervals.
- Spot check: the best clip for each brand visibly shows that brand.
```
