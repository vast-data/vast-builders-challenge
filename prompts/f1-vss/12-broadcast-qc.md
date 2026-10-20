# F1-VSS 12 - Broadcast QC

**Purpose:** automatically find broadcast faults (black frames, freezes, silence, missing timing graphics) in every incoming race.

Requires: `00-shared-context.md`.

---

## Paste into Cursor

```
Demo 12: broadcast QC.

Steps
1. Create table f1demo.qc_events (race_id, issue, start_ts, end_ts, severity).
2. Build a DataEngine function broadcast_qc on the chunk-land trigger so every incoming race is checked.
3. Run ffmpeg blackdetect (d=0.5), freezedetect (d=2), silencedetect (d=2, noise=-50dB).
4. Every 10 s, ask Cosmos3-Reason whether the timing graphics are on screen; flag gaps over 30 s during racing.
5. Cut a clip per issue, upload to Drive, write out/qc.json.

Done when an injected 3 s black frame in a test file is detected.
```
