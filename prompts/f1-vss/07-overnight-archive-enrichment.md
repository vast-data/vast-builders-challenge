# F1-VSS 7 - Overnight archive enrichment

**Purpose:** show the economics of enriching a back catalogue in bulk: hours of video in, GPU hours and cost per hour of video out, then search across every race.

Requires: demo 2, economics overlay.

---

## Paste into Cursor

```
Demo 7: overnight archive enrichment.

Steps
1. Enrich every archive race with the demo 2 racing-tag prompt using ingest-reingest-videos (all complete chunks per race). Run races in parallel up to the number of GPUs available, and monitor progress with retrieval-dashboard.
2. Track per file: duration, gpu_seconds, wall time (costs.track, asset_type="report").
3. Write out/archive.json: {files, hours_of_video, gpu_hours, cost_total, cost_per_hour_of_video, started_at, finished_at}.
4. Re-run the demo 2 queries across all races and append the results to out/search.json.

Done when cost per hour of video is printed and a query returns results from more than one race.
```
