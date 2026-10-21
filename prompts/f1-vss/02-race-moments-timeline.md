# F1-VSS 2 - Race moments timeline

**Purpose:** find the moments the captions can describe in each race and place them on a timeline.

Requires: `00-shared-context.md`.

---

## Paste into Cursor

```
Prompt ID: f1-vss/02-race-moments-timeline

Demo 2: race moments timeline.
Follow the F1 context prompt (f1-vss/00-shared-context) and build your own small app, including explore, search and the clip proxy.

Steps
1. List both races with retrieval-videos (explore). Race time = chunk_index x 30 s + offset.
2. A list of moment queries, editable in the app. Start with: "safety car leading the field", "aerial view of the circuit", "grandstand crowd", "driver in the car", "cars in the pit lane". Show the first four as Suggested searches buttons.
3. For each moment and race, run retrieval-search filtered to that race. Each hit is a 5 s segment. Add a minimum-score filter so a moment with no real hits (there is no safety car in formula-e_race) shows as none instead of weak markers.
4. Show a timeline per race (0 to 15 minutes) with the hits as markers. Clicking a marker plays that segment clip with retrieval-videos and shows its caption and search score.
5. Show a count per moment and race, and say clearly when a moment has no hits.

Done when both races show a timeline, at least three moments have hits, and every marker plays its clip.
```
