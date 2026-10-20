# DFL 2 - Growth-market reels

**Purpose:** auto-build player reels for growth markets (US, Brazil) with localized summaries and chapters.

Requires: `00-foundation.md`.

---

## Paste into Cursor

```
Using the DFL foundation, build the Market reels tab.

- Input: a market (US or Brazil) and a roster CSV (name, club, seasons, shirt numbers). Add data/americans.csv and data/brazilians.csv.
- Find segments per player with retrieval-search: name in captions, prompts like "<player> scores for <club>", plus season and club filters from the roster. Rank, then de-duplicate overlapping segments.
- Let me review and untick segments before rendering.
- Render the reel with ffmpeg (cut_clip helper), with a lower-third per clip (player, match, date).
- Write a summary and a chapter list with timecodes using Cosmos3-Reason (retrieval-videos synthesize for per-match context, or a direct chat call per the gpu README): English plus Spanish for US, Portuguese for Brazil.
- Store the reel in S3 under reels/ and add a row to a new table dfl.reels(reel_id, market, players, duration_s, s3_uri, created_ts).
- Metering: @metered("render", "minute") on render, @metered("license", "territory") when the reel is assigned to a market partner.

Acceptance: an "Americans in the Bundesliga" reel of 2 to 3 minutes renders end to end in under 10 minutes on the demo set, with summary and chapters in two languages.
```
