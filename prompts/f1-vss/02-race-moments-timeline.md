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
1. List both races with retrieval-videos (explore). Race time = chunk_index x 30 s + offset. Per-segment captions are in each chunk's `chunks[].timeline[].reasoning_content`, not the chunk-level field (the first segment only).
2. A list of moment queries shown in the app; the user can add and remove queries. Start with: "safety car leading the field", "aerial view of the circuit", "grandstand crowd", "driver in the car", "cars in the pit lane". Show the first four as Suggested searches buttons; clicking one runs that moment. A "Run all moments" button runs every query in the list, one at a time.
3. Each moment is one retrieval-search with metadata_filters {"camera_id": "f1-01"} and top_k 100, with a loading placeholder on that moment's row until it returns; split the hits into the two races by file name. The 100 hits are shared between the two races, so label the counts "top 100 across both races". A moment with no hit above the cutoff shows as none for that race.
4. Show a timeline per race (0 to the race's last chunk, about 46 or 50 minutes) with the hits as markers. Clicking a marker plays that segment clip with retrieval-videos and shows its caption and search score. The timeline shows the best-matching moments, not every occurrence; the per-segment captions (explore, `chunks[].timeline[]`) are the complete record if you need every occurrence.
5. Show a count per moment and race, and say clearly when a moment has no hits.

Done when both races show a timeline, at least three moments have hits, and every marker plays its clip.
```
