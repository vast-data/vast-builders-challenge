# F1-VSS 2 - Search every battle, overtake and logo

**Purpose:** natural-language search over every race for racing moments (overtakes, battles, pit stops, safety cars, logos) with sub-second latency.

Requires: `00-shared-context.md`. Later demos (3, 4, 6, 7, 9, 10) reuse its search wrapper and tags.

---

## Paste into Cursor

```
Demo 2: search every battle, overtake and logo.

The archive is already segmented, captioned and embedded, so do not build a new segment index.

Config
- config/queries.yaml: 10 demo queries, e.g. "every overtake into turn 1", "side by side battle", "pit stop", "safety car on track", "crash or spin", "podium celebration", "<brand> logo on the car".

Steps
1. Racing tags: use ingest-reingest-videos with a custom prompt so Cosmos3-Reason also returns tags from this fixed list: battle, overtake, pit_stop, safety_car, crash, spin, start, finish, podium, logo. Confirm the tags land with retrieval-videos (metadata).
2. Build search(query, k=5) as a thin wrapper over retrieval-search returning caption, tags, start/end timestamps and latency_ms. Expose it as a small FastAPI endpoint.
3. For each query in queries.yaml: run search, cut each result to a clip, upload to Drive, track cost with asset_type="query".
4. Write out/search.json: {queries: [{query, latency_ms, results: [{caption, tags, start_ts, end_ts, drive_preview_url}], cost}]}.

Done when
- At least 4 of the top 5 results for "overtake" are real overtakes.
- Median search latency is printed and under 1 s.
- The endpoint answers a new query typed live.
```
