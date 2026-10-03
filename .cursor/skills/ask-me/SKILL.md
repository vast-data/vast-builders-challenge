---
name: ask-me
description: >-
  Answer orientation questions about this repo and its skills — "how do I get started",
  "how do I ingest video", "how do I search", "what skills exist", "is everything
  working". Gives a short direct answer plus the exact skill to invoke next; never
  performs the action itself. Use when the user asks a general "how do I" / "what can
  I do" / "where do I start" question rather than giving a concrete task (a concrete
  task loads its own skill directly, e.g. "re-ingest the warehouse video").
---

# Ask me

Orientation, not execution. This skill turns a vague question into (1) a short plain-
language answer and (2) the exact skill to invoke for the real action. It never calls
APIs, runs curl, or performs ingest/search/deploy itself — that's the named skill's job.

Source of truth, in order: this file's routing table, then the repo docs
([README.md](../../../README.md), [BUILD_DAY.md](../../../BUILD_DAY.md),
[BEFORE_YOU_BUILD.md](../../../BEFORE_YOU_BUILD.md),
[ARCHITECTURE_REFERENCE.md](../../../ARCHITECTURE_REFERENCE.md)), then the other
skills' own `SKILL.md`/`README.md` files. If a question isn't in the table below, read
the relevant doc or skill file before answering — don't guess at an endpoint, scenario
name, or env var.

## "How do I get started?"

1. **Team + VM** — form a team, launch the VM from the workshop page, open this repo in
   Cursor (`cd ~/vast-builders-challenge && agent`). Covered in `BUILD_DAY.md` §1-2.
2. **Test drive the loop** — before building anything: search what's already indexed,
   ask a question about a video, then re-ingest one clip with a new prompt and search
   again. That one loop (search → ask → re-ingest → search) proves the whole stack
   works and is the fastest way to learn the skills. `BUILD_DAY.md` §4.
3. **Pick one idea and build it** — see the routing table below for the skill each step
   needs.
4. **Submit** — `submission` skill, near the end.

If step 1 or 2 fails, see "Is everything working?" below.

## Routing table

| They ask... | Point them at | One line |
|---|---|---|
| How do I get started / where do I start? | *(see above)*, then `BUILD_DAY.md` | Team → VM → test-drive loop → build → submit |
| How do I ingest / add a new video? | `ingest/upload-video` | Multipart upload of a **new** local file through the backend |
| How do I re-run / re-index a video that's already in the archive? | `ingest/reingest-videos` | Re-run detect→reason→embed→write with a new prompt/metadata |
| How do I re-ingest just one chunk / clip I saw in Explore? | `ingest/reingest-chunk` | Same, scoped to one chunk found from a description, filename, or card |
| What prompt presets / scenarios can I ingest with? | `retrieval/list-metadata` | Looks up live scenario + metadata options, don't guess them |
| How do I search the video archive? | `retrieval/search` | Hybrid text+visual search with filters (time, location, camera, tags) |
| How do I ask a question and get an answer (not a list of hits)? | `retrieval/agent-qa` | Grounded answer with evidence via the agent endpoints |
| How do I browse / play / summarize a specific video? | `retrieval/videos` | Explore timeline, stream playback, detections, LLM summary |
| What's indexed? Is ingest healthy? How many videos do I have? | `retrieval/dashboard` | Aggregate stats: counts, quality, objects, uploads by day |
| What filter values exist (locations, cameras, tags)? | `retrieval/list-metadata` | Valid `metadata_filters` keys/values before searching or uploading |
| Give me example queries / what's interesting right now? | `retrieval/suggest-prompts` | AI-generated prompt chips + key events |
| I want to check the database directly, not through the API | `retrieval/vastdb-read` | Direct VastDB read over an SSH tunnel, bypasses the backend/JWT |
| Are the GPU models (reasoning/embedding/detection) up? | `gpu/model-health` | Liveness/readiness per model, using each model's real health path |
| Health looks fine but reasoning/embeddings/detections are empty | `gpu/model-smoke-test` | Minimal real inference call per model to isolate the failure |
| How do I deploy my own app / mini-app / dashboard on top of this? | `deployment/deploy-app-no-registry` | On-cluster app at `/app` on the team host, no Docker build/push needed |
| How do I access my app once it's deployed? / it's not loading | *(see "Internal vs external URL" below)* — not a skill, not a redeploy | Two valid URLs for the same app; use the external one |
| How do I deploy or redeploy the retrieval stack itself? | `deployment/build-yamls` then `deployment/deploy` | Fill secrets/image tags, then `QUICK_DEPLOY.sh` — not needed for most teams, the stack is already up |
| Is everything working? / is the deployment healthy? | `deployment/health` | `kubectl get pods`, backend `/health`, effective config |
| Something's broken and I need help | `ask-cosmos` | Runs the health check, triages the common causes, drafts a help note — never posts it |
| How do I submit our project? | `submission` | Walks each section, writes `SUBMISSION.md` |
| What skills exist / what can this repo do? | *(this table)*, or the group `README.md` files under `.cursor/skills/*/README.md` | — |

## Internal vs external URL (deployed apps)

Once `deployment/deploy-app-no-registry` finishes, the app is reachable at **two** URLs.
Don't treat one as broken just because the other works — they're the same app.

| URL | Works from | Use it when |
|---|---|---|
| `http://video-lab-team-<N>.cosmos.vastdata.com/app/` | Inside the workshop VM only | This is the real Ingress host the deploy skill configures. It's correct as-is — never change it, and it's expected not to load from outside the VM. |
| `https://team-<N>-app.thecosmoslabs.com/app/` | Your own laptop, anywhere | **Recommended for demos and day-to-day use.** Goes through Cloudflare and loads noticeably faster than tunneling through the VM. |

Swap `<N>` for your team number in both. If someone says "my app isn't loading," ask
which URL they used before assuming the deploy itself failed — most of the time it's
just the VM-internal one being tried from a laptop, or vice versa.

This is purely about *which address to open in a browser* — it doesn't change how the
app is deployed or verified, so `deployment/deploy-app-no-registry` itself is unchanged
and still built around the internal host.

## Questions that need the docs, not a skill

These aren't actions, so don't route to a skill — read and answer from the doc:

| They ask... | Read |
|---|---|
| What video do we actually have? What should I demo? | `ARCHITECTURE_REFERENCE.md` → Video corpus section (packs, camera IDs, example queries) |
| What models run this stack, and what does each one do? | `ARCHITECTURE_REFERENCE.md` → Models section |
| Where do my credentials / endpoints come from? | `config.example` lists every env var; real values are in `/config/<team>.config` on the VM — never search the repo's `team-configs/` |
| What's the overall architecture / pipeline? | `ARCHITECTURE_REFERENCE.md` → Data Engine section |
| What's expected before build day? | `BEFORE_YOU_BUILD.md` |

## How to answer

1. Match the question to a row above (loosely — "how do I look for X in the videos"
   means search, not literal wording).
2. Give 1-3 sentences of direct answer, in plain language, no API detail — that detail
   lives in the target skill.
3. Name the skill to invoke next (or the doc section, for the non-action questions),
   so the user or agent can load it immediately.
4. If nothing matches, don't invent an answer: skim `BUILD_DAY.md` or the relevant
   group `README.md` under `.cursor/skills/`, then answer from what's actually there.
5. Never execute the target skill yourself unless the user's next message is the
   concrete task — this skill's job ends at pointing the way.
