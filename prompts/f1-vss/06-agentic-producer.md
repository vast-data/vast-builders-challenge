# F1-VSS 6 - Agentic producer

**Purpose:** an agent that turns an editorial brief ("60 second package on the battle for P3") into a finished cut plus a timed voiceover script, with a readable tool-call log.

Requires: demos 2 and 3.

---

## Paste into Cursor

```
Demo 6: agentic producer.

Config
- config/briefs.yaml: ["60 second package on the battle for P3", "30 second social cut of the start"].

Steps
1. Build an agent on Cosmos3-Reason with tools: search_segments(query) using the demo 2 wrapper (retrieval-search), ask(question) using retrieval-agent-qa, list_periods(race_id) from f1demo.periods, cut_clip(start_ts, end_ts), assemble(clips, target_seconds), write_script(clips, seconds).
2. For each brief: plan, call tools, assemble the MP4, write a voiceover script timed to the edit.
3. Log every tool call (name, args, latency) into the JSON.
4. Upload to Drive, track cost with asset_type="package", write out/producer.json: {briefs: [{brief, drive_preview_url, script, clips, tool_calls, cost}]}.

Done when each package matches its brief and target length, and the tool-call log is readable on screen.
```
