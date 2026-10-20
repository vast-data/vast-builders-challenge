# 2026 GTC Berlin workshop: demo build prompts

Cursor build prompts for the GTC Berlin workshop / hackathon lab. Two tracks:

| Folder | Track | Contents |
|---|---|---|
| [`dfl-archive/`](dfl-archive/) | Bundesliga (DFL) football archive | `00-foundation.md` (run first), then 5 demos |
| [`f1-vss/`](f1-vss/) | F1 Academy / Formula E racing footage on the VSS stack | `00-shared-context.md` and `00-economics-overlay.md` (run first), then 12 demos |

Idea catalog (project names, descriptions, overlap with earlier SF / NYC / London hackathon submissions): [berlin-ideas tab](https://docs.google.com/spreadsheets/d/1nwfOfeOgFUw0fkhu311kjUiChzyFDJciAAdxpT1M6kk/edit#gid=1627914172).

Original ideas and prompts: Jason Hammons (`cursor-prompts.md` for DFL, `vss-demo-builds.html` for F1-VSS), shared over Slack.

## What changed from the originals

The original prompts were written for a from-scratch build, so they spelled out storage prefixes, DataEngine triggers, database DDL, segmentation, captioning and embedding by hand. These versions assume Cursor is opened on the [vast-builders-challenge](https://github.com/relaxedtomato/vast-builders-challenge) starter repo, whose `.cursor/` folder already loads skills for the running VSS stack. Each prompt now names the skill to use, or states the outcome and lets the skill handle the mechanics. Demo-specific logic (fields, scoring, phase rules, acceptance criteria) is unchanged.

### Skills the prompts rely on

| Need | Skill (in `.cursor/skills/`) |
|---|---|
| Ground rules, never hardcode creds | `rules/build-day.mdc` |
| Auth to the backend | `retrieval-login` |
| Search the indexed archive | `retrieval-search` |
| Grounded Q&A over video | `retrieval-agent-qa` |
| Playback, per-video summary, YOLO detections | `retrieval-videos` |
| Filter fields and values | `retrieval-list-metadata` |
| Ingest health and stats | `retrieval-dashboard` |
| Raw VAST DataBase reads / own tables | `retrieval-vastdb-read` |
| Add a new MP4 | `ingest-upload-video` |
| Re-run indexed footage with a custom prompt | `ingest-reingest-videos`, `ingest-reingest-chunk` |
| Custom DataEngine functions and triggers | `dataengine-edit-function` → `dataengine-build-function` → `dataengine-functions` → `dataengine-triggers` → `dataengine-pipeline-manifest` |
| Model endpoints | gpu README, `gpu-model-health`, `gpu-model-smoke-test` |
| Stuck | `ask-cosmos` |
| Wrap up | `submission` |

### Model mapping

The starter stack runs a fixed model set. The originals named other models; the refactored prompts use these instead:

| Original prompt said | Starter stack uses |
|---|---|
| Marengo embeddings, "VSS embedding model" | Cosmos-Embed1 (256-dim, text and video) |
| Pegasus, "VSS VLM", "VSS LLM" | Cosmos3-Reason |
| "VSS ASR" | Canary-1B (optional, not in the default pipeline) |
| Grounding DINO open-vocabulary detection | YOLO11 (fixed classes) for objects such as cars; Cosmos3-Reason frame questions for brands/logos |
| SAM2 tracking | YOLO11 boxes linked across frames (IoU tracking) |
| PaddleOCR | Cosmos3-Reason reading on-screen graphics; PaddleOCR kept as a fallback |
| Custom 8 s / 10 s segment index | The existing VSS segment index (already captioned and embedded) |
