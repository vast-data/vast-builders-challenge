# DFL 1 - Across the eras

**Purpose:** search the same moment across the indexed Bundesliga matches and compare it season by season.

Requires: `00-foundation.md` (context only).

---

## Paste into Cursor

```
Prompt ID: dfl-archive/01-across-the-eras

Build a search that compares the same moment across the indexed Bundesliga matches. Follow the DFL context prompt (dfl-archive/00-foundation) and build your own small app, including search and the clip proxy (this demo does not need explore).

Steps
1. A search box using retrieval-search. Suggested searches: "player celebrates a goal", "players shake hands before kickoff", "teams walk out with mascots", "fans waving scarves in the stands".
2. This demo compares every season in one view, so it always searches all eras: send camera_id only, with no location filter, and do not add an era control. Run the query at top_k 50 (hits spread over many seasons) and group the ranked list by season, oldest first, with a chip per season that appears in the results; hide seasons with no hits. Take the season from the file name. Each card shows the match, competition (when it differs from Bundesliga — the set includes a cup final and a 2. Bundesliga match), time in the match, caption and score, and plays the segment clip with retrieval-videos.
3. Show a hit count per season.

Done when each suggested search returns results at or above the score cutoff in at least two seasons at top_k 50, and every card plays.
```
