# F1-VSS 7 - Archive overview and cross-race search

**Purpose:** show how much race footage is indexed and search across every race at once.

Requires: `00-shared-context.md`.

---

## Paste into Cursor

```
Prompt ID: f1-vss/07-archive-overview

Demo 7: archive overview and cross-race search.
Follow the F1 context prompt (f1-vss/00-shared-context) and build your own small app, including explore, search and the clip proxy.

Steps
1. List the races with retrieval-videos (explore): only the two whose names end in _race (f1-academy_race and formula-e_race). Show chunk count, about how many minutes of video (chunks x 30 s, nominal) and indexed segments. Check ingest health with retrieval-dashboard.
2. App tab "Archive": a table of the two races with those numbers.
3. App tab "Search": one search box over all races with retrieval-search. Group results by race and play each result's segment clip with retrieval-videos.
4. Do not re-ingest the archive. Re-ingest is limited to 3 chunks and 30 seconds per request (one chunk in practice).

Done when the minutes of video per race are shown and a query returns results from more than one race.
```
