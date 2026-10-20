# F1-VSS 12 - Broadcast QC

**Purpose:** automatically find broadcast faults (black frames, freezes, silence, missing timing graphics) in every incoming race.

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
2. In the app, list one race's chunks with retrieval-videos (explore), fetch each 30 s chunk file server-side, and check it locally. Nothing is uploaded or re-ingested.
3. Run ffmpeg blackdetect (d=0.5), freezedetect (n=-60dB, d=2) and silencedetect (d=2, noise=-50dB). Ignore a freeze that overlaps a black segment. Severity: high for black or freeze, medium for silence.
4. The app lists every issue with its time and severity, and plays the affected segment clip through the proxy.
5. Self-test button: make a local test copy of one chunk with a 3 s black frame injected, run the checks on it and on an untouched copy, and show both results side by side.

Done when the 3 s black frame is detected in the test copy and the untouched copy reports nothing.
```
