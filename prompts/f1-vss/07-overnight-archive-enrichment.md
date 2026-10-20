# F1-VSS 7 - Archive overview and cross-race search

**Purpose:** show how much race footage is indexed and search across every race at once.

Requires: `00-shared-context.md`.

---

## Paste into Cursor

```
Prompt ID: f1-vss/07-overnight-archive-enrichment

Demo 7: archive overview and cross-race search.

Steps
1. List every race with retrieval-videos (explore): chunk count, hours of video (chunks x 30 s) and indexed segments. Check ingest health with retrieval-dashboard.
2. App tab "Archive": a table of races with those numbers.
3. App tab "Search": one search box over all races with retrieval-search. Group results by race and play each result's segment clip with retrieval-videos.
4. Do not re-ingest the archive. Re-ingest is limited to 3 chunks and 30 seconds per request.

Done when the hours of video per race are shown and a query returns results from more than one race.
```
