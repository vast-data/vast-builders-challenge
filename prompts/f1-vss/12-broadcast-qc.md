# F1-VSS 12 - Broadcast QC

**Purpose:** automatically find broadcast faults (black frames, freezes, silence, missing timing graphics) in every incoming race.

Requires: `00-shared-context.md`.

---

## Paste into Cursor

```
Prompt ID: f1-vss/12-broadcast-qc

Demo 12: broadcast QC.

Steps
1. Create table f1demo.qc_events (race_id, source, issue, start_ts, end_ts, severity) with vast-database-vastdb-write. Times are relative to the file.
2. In the app, list one race's chunks with retrieval-videos (explore), fetch each through its playback URL, and check it locally. Nothing is uploaded or re-ingested.
3. Run ffmpeg blackdetect (d=0.5), freezedetect (n=-60dB, d=2) and silencedetect (d=2, noise=-50dB). Ignore a freeze that overlaps a black segment.
4. Optional timing-graphics check: flag a gap over 30 s where consecutive racing segments' captions mention no timing graphics. Captions are the only signal, so expect false alarms on replays.
5. The app lists every issue with its time, severity and the affected segment clip, played with retrieval-videos.

Done when
- A 3 s black frame injected into a locally made test copy of a chunk is detected.
- The same check on an untouched copy reports nothing.
```
