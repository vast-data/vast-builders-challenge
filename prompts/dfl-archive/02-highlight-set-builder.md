# DFL 2 - Highlight set builder

**Purpose:** curate a labelled clip set for a topic across the five indexed Bundesliga matches, with a summary card.

Requires: `00-foundation.md` (context only).

---

## Paste into Cursor

```
Prompt ID: dfl-archive/02-highlight-set-builder

Build a curated clip set for a topic, across the five indexed Bundesliga matches. Follow the DFL context prompt (dfl-archive/00-foundation) and build your own small app, including explore, search and the clip proxy.

Steps
1. Enter a topic. Suggested searches: "player celebrates a goal", "goalkeeper dives to stop a shot", "teams walk out with mascots", "players shake hands before kickoff". Search it with retrieval-search and show candidates from all matches, 5 s each.
2. Each candidate has Accept and Reject buttons and plays its clip with retrieval-videos. Merge neighbouring segments from the same match into one item.
3. A "Set" panel lists accepted items with match, season, time range and caption.
4. A dataset card, shown in the app: topic, number of items, total seconds, items per match and season, and how many were rejected.
5. Save the set to the dfl schema with vast-database-vastdb-write (a table, not a file).

Done when a set of at least 8 accepted items is saved and the card shows counts per match.
```
