# Demo prompts

Cursor prompts for two video sources already indexed on the starter stack: Bundesliga football and Formula racing. Open the repo in Cursor, then paste the block under "Paste into Cursor" from a prompt file into the agent panel.

Run a track's `00` context prompt first. It builds no app; it sets the rules and known pitfalls that every demo in the track follows. Then run a demo. Each demo builds its own small app.

| Track | Prompt | What it gives you |
|---|---|---|
| [`dfl-archive/`](dfl-archive/) | `00-foundation` | Context and a one-time era setup: match IDs, filters, eras, licensing rules |
| | `01-across-the-eras` | The same moment searched across the indexed matches, grouped by season |
| | `02-highlight-set-builder` | Accept and reject clips for a topic, then save the set with a summary card |
| | `03-rights-aware-licensing-storefront` | A storefront that shows rights, partner and price per clip, and meters licenses |
| [`f1-vss/`](f1-vss/) | `00-shared-context` | Context only: race scoping, clip proxy, conventions |
| | `01-sponsor-exposure-ledger` | Seconds on screen per sponsor, with a best clip each |
| | `02-race-moments-timeline` | Search moments per race and see them as markers on a timeline |
| | `07-archive-overview` | The indexed races at a glance, and one search across both |
| | `11-live-incident-alerts` | A replayed race that raises safety-car and incident alerts |
| | `12-broadcast-qc` | Black, freeze and silence checks, with a self-test |

## What to know about the footage

- Formula racing: two races (`f1-academy_race`, about 46 min; `formula-e_race`, about 50 min).
- Bundesliga: more than 30 full matches, about 100 minutes each, from 1970-71 to 2026-27.
- Everything is stored as 30 s chunks of 5 s segments. A search can take several seconds.

## Skills the prompts use

| Need | Skill (in `.cursor/skills/`) |
|---|---|
| Search the indexed footage | `retrieval-search` |
| Playback, captions, detections | `retrieval-videos` |
| Grounded Q&A | `retrieval-agent-qa` |
| Ingest health and stats | `retrieval-dashboard` |
| Read and write your own tables | `vast-database-vastdb-read`, `vast-database-vastdb-write` |
| Faster football searches (one-time setup) | `vast-database-football-eras` |
| Stuck | `ask-help` |

Tip: when you are only changing how the app looks, ask your agent to mock the responses for rapid UI iteration. Changes are quicker to check, and it saves shared GPU time. Ask it to turn the mock off when you are done.

Re-ingest is not available, and the prompts do not deploy DataEngine functions. Uploading new video works but is not recommended, because it uses GPUs every team shares; if you need your own footage, `ingest-upload-video` uploads a clip of 30 s or less.
