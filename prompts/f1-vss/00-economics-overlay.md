# F1-VSS 0b - Economics overlay (run right after the scaffold)

**Purpose:** a live cost rollup (GPU cost per clip, query, report, package, reel and per hour of video) that every other demo feeds.

Requires: `00-shared-context.md`.

---

## Paste into Cursor

```
Demo: economics overlay.

1. Create a scheduled DataEngine function costs_rollup that runs every 60 seconds (dataengine-edit-function for the code, dataengine-triggers for the Schedule trigger, dataengine-pipeline-manifest to wire it).
2. Read f1demo.job_costs and config/pricing.yaml.
3. Per asset type (clip, query, report, package, reel): count, total gpu_seconds, cost per asset (gpu_seconds / 3600 x hourly rate).
4. Per race: total cost, hours of video processed (source duration from retrieval-videos), cost per hour of video.
5. Write out/costs.json: {rate, per_asset_type: [...], per_race: [...], sale_price: {clip: null, query: null, report: null, package: null, reel: null}}. Leave sale_price null for me to fill. No margin percentages.

Done when costs.json updates within 60 s of any job finishing, and a single clip shows its own gpu_seconds and cost.
```
