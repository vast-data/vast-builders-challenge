# F1-VSS 1 - Sponsor exposure ledger

**Purpose:** measure on-screen seconds per sponsor in a race and produce evidence frames and a best clip per brand.

Requires: `00-shared-context.md`.

---

## Paste into Cursor

```
Demo 1: sponsor exposure ledger.

Config
- config/brands.yaml: list of {brand, prompts: ["<brand> logo", "<brand> text"], category}. Start with the sponsors visible on the cars and track boards.

Steps
1. Create table f1demo.sponsor_exposure (race_id, brand, start_ts, end_ts, seconds, max_screen_area_pct, mean_confidence, best_frame_uri).
2. Build a DataEngine function sponsor_ledger on the segment-land trigger so every newly indexed segment is scanned.
3. Handler: sample frames at 2 fps. YOLO11 has fixed classes, so ask Cosmos3-Reason per frame which configured brands are visible, with a confidence and approximate bbox. Keep detections with confidence >= 0.35.
4. Merge consecutive detections of the same brand into intervals when the gap is under 1.0 s; drop intervals under 1.0 s.
5. Insert intervals into sponsor_exposure. Save the highest-confidence frame per interval as JPG to clips/sponsor/.
6. Per brand: cut a 30 s clip around its longest interval; upload the top 5 frames and the clip to Drive.
7. Wrap steps 3 to 6 in costs.track(asset_type="report").
8. Write out/sponsor.json: {race_id, brands: [{brand, total_seconds, intervals, top_frames: [drive_urls], best_clip: drive_preview_url, cost}]}.

Done when
- Total seconds per brand sum correctly from intervals.
- Spot check: the best clip for each brand visibly shows that brand.
- Report cost appears in costs.json.
```
