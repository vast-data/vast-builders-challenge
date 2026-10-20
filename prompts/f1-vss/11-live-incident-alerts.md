# F1-VSS 11 - Live incident alerts

**Purpose:** watch a race feed and raise a confirmed alert (with clip) for crashes, spins, yellow flags and safety cars within seconds.

Requires: `00-shared-context.md`.

---

## Paste into Cursor

```
Demo 11: live incident alerts.

Steps
1. Simulate live: feed the race in real-time 5 s chunks to Cosmos3-Reason (see the gpu README) with the question "Is there a crash, spin, yellow flag or safety car? Answer with one label or none."
2. Confirm an alert only if two consecutive chunks agree.
3. On alert: cut a 20 s clip ending at the detection, upload to Drive, post to a Slack webhook (config/slack.yaml).
4. Write out/alerts.json: {alerts: [{type, race_ts, detected_after_s, drive_preview_url}]}.

Done when every safety car in the race raises an alert with under 15 s latency.
```
