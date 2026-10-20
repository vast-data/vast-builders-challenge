# F1-VSS 10 - Instant history

**Purpose:** while commentary runs live, detect mentions of drivers, past races or records and surface matching archive clips within seconds.

Requires: demos 2 and 7 (archive indexed).

---

## Paste into Cursor

```
Demo 10: instant history.

Steps
1. Simulate live: stream the race audio through Canary-1B ASR in real-time 5 s chunks.
2. Extract mentions of drivers, past races or records with Cosmos3-Reason (prompt: extract names, years, circuits, "last time" phrases).
3. For each mention: search the archive with retrieval-search and return the top 3 clips.
4. Record time from mention to match.
5. Upload matched clips to Drive, write out/history.json: {mentions: [{ts, quote, entities, matches: [drive_preview_url], latency_ms}]}.

Done when median mention-to-match time is under 5 s.
```
