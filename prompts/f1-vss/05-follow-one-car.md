# F1-VSS 5 - Follow one car

**Purpose:** track a single car through a race and auto-cut a 16:9 reel plus a 9:16 vertical crop that keeps the car in frame.

Requires: `00-shared-context.md`, demo 2 tags.

---

## Paste into Cursor

```
Demo 5: follow one car.

Config
- config/cars.yaml: [{car: "7", driver: "<name>", livery: "pink and white car with number 7"}].

Steps
1. Create table f1demo.car_appearances (race_id, car, start_ts, end_ts, mean_bbox, confidence).
2. Build a DataEngine function car_follow on the segment-land trigger.
3. Start from the YOLO11 car detections already stored per segment (retrieval-videos detections). Pick the target car among them by asking Cosmos3-Reason whether each detected car matches the livery prompt, then link boxes into tracks across frames (IoU tracking is fine); keep tracks over 2 s.
4. Insert appearances. Rank by duration x on-screen size, boosted by demo 2 tags (overtake, battle).
5. Build a 60 s 16:9 reel from the top appearances, and a 9:16 version cropped around the tracked bbox (smoothed with a 0.5 s moving average).
6. Upload both to Drive, track cost with asset_type="reel", write out/cars.json.

Done when the car is in frame in at least 90% of the vertical reel.
```
