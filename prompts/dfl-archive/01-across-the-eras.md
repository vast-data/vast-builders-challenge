# DFL 1 - Across the eras

**Purpose:** search the same moment across the five indexed Bundesliga matches and compare it season by season.

Requires: `00-foundation.md` (context only).

---

## Paste into Cursor

```
Prompt ID: dfl-archive/01-across-the-eras

Build a search that compares the same moment across the five indexed Bundesliga matches. Follow the DFL context prompt (dfl-archive/00-foundation) and build your own small app, including explore, search and the clip proxy.

Steps
1. A search box using retrieval-search. Suggested searches: "player celebrates a goal", "players shake hands before kickoff", "teams walk out with mascots", "fans waving scarves in the stands".
2. Run the query across all matches and group the results into one column per season (2008-09, 2010-11, 2011-12, 2017-18, 2026-27), taking the season from the file name. Each card shows the match, time in the match, caption and score, and plays the segment clip with retrieval-videos.
3. Show a hit count per season. If a season has none, say so.
4. Show how long each search took.

Done when each starter query returns results in at least two seasons and every card plays.
```
