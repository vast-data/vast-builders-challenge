# F1-VSS 3 - Period clipper

**Purpose:** automatically split a race into phases (grid, start, safety car, pit window, final laps, chequered flag, podium) and publish one clip per phase.

Requires: `00-shared-context.md`, demo 2 tags.

---

## Paste into Cursor

```
Demo 3: period clipper.

Phases: grid, start, opening_laps, race, safety_car, pit_window, final_laps, chequered_flag, podium.

Steps
1. Create table f1demo.periods (race_id, phase, start_ts, end_ts, confidence, evidence).
2. Build a DataEngine function period_clipper that runs when a race finishes indexing. Reuse the demo 2 tags on the indexed segments.
3. Signals, all timestamped:
   a. On-screen graphics every 2 s (lap counter "LAP x/y", "SAFETY CAR", flag icons): ask Cosmos3-Reason to read them from the frame, or use PaddleOCR if the VLM is unreliable on the lap counter.
   b. Commentary ASR with Canary-1B (see the gpu README); keyword-spot "lights out", "safety car", "pit", "chequered flag", "podium".
   c. Racing tags from demo 2.
4. Phase rules: start = first "lights out" or lap 1 appears; safety_car = from the "SAFETY CAR" graphic until it disappears; final_laps = last 3 laps by lap counter; chequered_flag = flag icon or commentary; podium = after the flag when tags say podium. Fill gaps with race.
5. Insert periods with confidence (share of signals that agree) and evidence (which signals fired).
6. Cut each phase to an MP4 (cap at 3 minutes; for long phases take the highest-scoring 3 minutes), upload to Drive, copy to S3 publish/. Track cost with asset_type="clip".
7. Write out/periods.json: {race_id, phases: [{phase, start_ts, end_ts, confidence, evidence, drive_preview_url, cost}], processing_seconds}.

Done when
- Phases are in order and do not overlap.
- Start and chequered flag are within 10 s of the real moments.
- Time from file landing to first clip on Drive is printed.
```
