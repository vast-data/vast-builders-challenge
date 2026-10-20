# Demo prompts

Cursor prompts for two video sources already indexed on the starter stack: Bundesliga football and Formula racing. Open the repo in Cursor, then paste the block under "Paste into Cursor" from a prompt file into the agent panel.

Run a track's `00` context prompt first. It builds nothing; it sets the rules and known pitfalls that every demo in the track follows. Then run a demo. Each demo builds its own small app.

| Track | Prompt | What it gives you |
|---|---|---|
| [`dfl-archive/`](dfl-archive/) | `00-foundation` | Context only: match IDs, filters, licensing rules |
| | `03-rights-aware-licensing-storefront` | A storefront that shows rights, partner and price per clip, and meters licenses |
| [`f1-vss/`](f1-vss/) | `00-shared-context` | Context only: race scoping, clip proxy, conventions |
| | `01-sponsor-exposure-ledger` | Seconds on screen per sponsor, with a best clip each |
| | `07-archive-overview` | The indexed races at a glance, and one search across both |
| | `11-live-incident-alerts` | A replayed race that raises safety-car and incident alerts |
| | `12-broadcast-qc` | Black, freeze and silence checks, with a self-test |

## What to know about the footage

- Formula racing: two races (`f1-academy_race`, `formula-e_race`), about the first 15 minutes of each broadcast.
- Bundesliga: five matches of about 15 minutes each, from 2008-09 to 2026-27.
- Everything is stored as 30 s chunks of 5 s segments. Search takes about 3 s.

## Skills the prompts use

| Need | Skill (in `.cursor/skills/`) |
|---|---|
| Search the indexed footage | `retrieval-search` |
| Playback, captions, detections | `retrieval-videos` |
| Grounded Q&A | `retrieval-agent-qa` |
| Ingest health and stats | `retrieval-dashboard` |
| Re-run indexed footage with a custom prompt | `ingest-reingest-videos` (max 3 chunks and 30 seconds per request) |
| Read and write your own tables | `vast-database-vastdb-read`, `vast-database-vastdb-write` |
| Stuck | `ask-cosmos` |

Uploading new video is disabled, and the prompts do not deploy DataEngine functions.
