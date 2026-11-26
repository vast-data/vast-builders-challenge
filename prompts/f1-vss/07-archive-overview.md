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
1. List the races with retrieval-videos (explore): explore with location=england returns only the two races, f1-academy_race and formula-e_race; group them by race. Show chunk count, about how many minutes of video (chunks x 30 s, nominal) and indexed segments (count the timeline[] entries per race). Show ingest health from retrieval-dashboard as one neutral line: indexed clips and clips still pending. These are whole-stack figures, so a pending count above zero is not a fault in the two races; do not show it as a warning or an error.
2. App tab "Archive": a table of the two races with those numbers.
3. App tab "Search": one search box over all races with retrieval-search. Group results by race and play each result's segment clip with retrieval-videos. Suggested searches: "driver in the car", "aerial view of the circuit", "sponsor logos on the barriers", "grandstand crowd". Search with metadata_filters {"camera_id": "f1-01"} (it covers both races), split the hits by file name (original_video / source contains f1-academy_race or formula-e_race), and merge by race: an unscoped search for "grandstand crowd" returns only football.

Done when the minutes of video per race are shown and a query returns results from more than one race.
```
