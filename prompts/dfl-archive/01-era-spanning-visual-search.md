# DFL 1 - Era-spanning visual search

**Purpose:** search the Bundesliga archive by text or by example clip and show the same kind of moment side by side across decades.

Requires: `00-foundation.md`.

---

## Paste into Cursor

```
Using the DFL foundation (schema dfl, meter.py, app.py), build the Search tab.

- Text search: use retrieval-search over the indexed archive, joined to dfl.assets on original_video.
- Clip search: upload a short clip or press "Find similar" on any result; embed it with Cosmos-Embed1 (video input, see the gpu README) and search with the same filters.
- Filters: era (multi-select), competition, home/away team, season range. Resolve filter fields with retrieval-list-metadata and push them into the search request (metadata_filters), not into Python after the fact.
- Results: group by era in columns so the same kind of moment appears side by side across decades. Each card shows thumbnail, match, date, caption and plays from start_s via retrieval-videos.
- Metering: @metered("search", "query") on each search, @metered("retrieve", "clip") when a result plays.
- Show query latency on screen.

Test queries: "diving header in the snow", "goalkeeper saves a penalty", "fans on the pitch after the final whistle", and clip search from a modern goal to historic goals.

Acceptance: the first query returns results from at least two decades; latency under one second on the demo set; the Meter tab shows the events.
```
