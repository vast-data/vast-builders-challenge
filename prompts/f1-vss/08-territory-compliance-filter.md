# F1-VSS 8 - Territory compliance filter

**Purpose:** flag segments showing brands banned in a market (alcohol in FR, betting elsewhere) and produce a blurred, market-safe version.

Requires: demo 1 (sponsor_exposure with bboxes).

---

## Paste into Cursor

```
Demo 8: territory compliance filter.

Config
- config/markets.yaml: [{market: "FR", banned_categories: ["alcohol"]}, {market: "<x>", banned_categories: ["betting"]}]. Categories come from brands.yaml.

Steps
1. Use f1demo.sponsor_exposure from demo 1. If it does not keep per-frame bboxes, add f1demo.detections (race_id, ts, brand, bbox).
2. For each market: find indexed segments that overlap banned-brand intervals.
3. For one sample clip per market: export the original and a version with the logo region blurred (ffmpeg boxblur on the tracked bbox, padded 10%).
4. Upload both to Drive, write out/compliance.json: {markets: [{market, flagged_segments, before_url, after_url}]}.

Done when the blurred clip shows no readable banned logo.
```
