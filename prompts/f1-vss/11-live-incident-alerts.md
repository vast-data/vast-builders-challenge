# F1-VSS 11 - Live incident alerts

**Purpose:** watch a race feed and raise a confirmed alert (with clip) for crashes, spins, yellow flags and safety cars as a race replays.

Requires: `00-shared-context.md`.

---

## Paste into Cursor

```
Prompt ID: f1-vss/11-live-incident-alerts

Demo 11: live incident alerts.
Follow the F1 context prompt (f1-vss/00-shared-context) and build your own small app, including explore, search and the clip proxy.

Steps
1. Simulate live: replay one race's indexed 5 s segments in order (retrieval-videos explore, timeline), pacing the replay so each segment is processed when it would have finished airing.
2. For each segment, read its existing caption (reasoning_content) and flag a crash, spin, yellow flag or safety car when the caption mentions one from a keyword list you write (include "SAFETY CAR" and "YELLOW FLAG" banners). Ignore negations ("no safety car") and mentions of a replay. Offer a fast-replay option that runs the replay at 5x speed. Only the pipeline's models are available, so use the captions, not new model calls.
3. Confirm a safety car or yellow flag only if two consecutive segments agree. A crash or spin may alert on a single hit. After an alert, keep that incident open until a caption says "green flag" or "safety car ending", so each incident raises one alert.
4. The app shows a live alert feed. Each alert has its type, race time and the segment clip, played with retrieval-videos.
5. Add a "Find an incident" search with Suggested searches: "safety car leading the field", "crash or collision", "cars in the pit lane", scoped to the replay race.

Done when the race's safety-car period raises exactly one alert within 15 s of the first caption that mentions it (the on-screen banner may appear earlier, so latency measured from the banner is longer), and the app reports how many crashes and yellow flags were caught.
```
