# F1-VSS 12 - Broadcast QC

**Purpose:** find broadcast faults (black frames, freezes, silence) in a race, with a self-test that proves the checks work.

Requires: `00-shared-context.md`.

---

## Paste into Cursor

```
Prompt ID: f1-vss/12-broadcast-qc

Demo 12: broadcast QC.
Follow the F1 context prompt (f1-vss/00-shared-context) and build your own small app, including explore, search and the clip proxy.

The indexed footage has no real faults, so the self-test is the demo.

Steps
1. Create table f1demo.qc_events (race_id, source, issue, start_ts, end_ts, severity) with vast-database-vastdb-write. Times are relative to the file. Delete a race's rows before re-running it.
2. On the VM, list one race's chunks with retrieval-videos (explore) and fetch each 30 s chunk file; run the checks there (step 3), not in the app. Nothing is uploaded or re-ingested.
3. Run ffmpeg blackdetect (d=0.5), freezedetect (n=-60dB, d=2) and silencedetect (d=2, noise=-50dB) on the VM, not in the deployed app (it has no ffmpeg). Ignore a freeze that overlaps a black segment. Severity: high for black or freeze, medium for silence. Write the events into qc_events; the app reads them from there.
4. The app lists every issue with its time and severity, and plays the affected segment clip through the proxy.
5. Self-test button: on the VM, make a local test copy of one chunk with a 3 s black frame injected, run the checks on it and on an untouched copy, and write or show both results so the app can display them side by side.
6. Suggested searches for finding a moment to check: "grandstand crowd", "aerial view of the circuit", "driver in the car", "cars in the pit lane".

Done when the 3 s black frame is detected in the test copy and the untouched copy reports nothing.
```
