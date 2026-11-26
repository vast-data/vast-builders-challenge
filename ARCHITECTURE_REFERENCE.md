# Builders Challenge Reference

A deeper dive into the architecture behind [README.md](README.md) — the models, the
DataEngine pipeline, and the full video corpus. Team setup and credentials are covered
there; this doc doesn't repeat them.

---

## Models (NVIDIA on CoreWeave)

Inference for the pipeline runs on shared **GPU endpoints** (NVIDIA Cosmos + YOLO + Canary). You don’t deploy the models yourself, and you don't call them directly either — they're reachable only through the pipeline API.

| Model | Role in VSS |
|-------|-------------|
| **NVIDIA Cosmos3-Reason** (`nvidia/cosmos3-reason`) | Video understanding / reasoning over segments |
| **YOLO11** (`yolo11s`, Ultralytics) | Object detection (bounding boxes / labels) |
| **NVIDIA Cosmos Embed1** (`nvidia/cosmos-embed1`) | Text and visual embeddings (256-dim) for hybrid search |
| **NVIDIA Canary-1B** (`nvidia/canary-1b`) | Speech-to-text (ASR) + speech translation — **not** Cosmos; NeMo audio model |

Ingest and search call **Cosmos3-Reason**, **YOLO11**, and **Embed1** through your pipeline and backend today.

**Canary-1B** is not wired into the current VSS pipeline. If you want audio transcripts, spoken-word search, or speech translation in your demo, that would need to be wired in through the pipeline API, not a direct call to the model.

---

## Data Engine

### VSS Blueprint

Your team’s ingest runs as a **VAST DataEngine** serverless pipeline. A video chunk lands in S3, then functions run in sequence until searchable rows exist in VastDB.

```
S3 chunks (bucket)  →  Segmenter  →  S3 segments (bucket)
                                           ↓
                                        Detector → Reasoner → Embedder → VastDB writer
```

A separate **events / prompt-suggester** function runs on a schedule and feeds UI suggestions.

![VAST DataEngine pipeline](docs/hackathon/vss-pipeline.png)

**VAST DataEngine (pipeline’s tab)** — view the pipeline’s flow, logs, and traces. Treat the graph as given for the challenge (don’t rebuild functions or redeploy the pipeline).

| Function | What it does |
|----------|--------------|
| **Segmenter** | Splits each uploaded chunk into short fixed-length clips and writes them to the segments bucket. **Builders challenge:** organizers already used the Segmenter to pre-ingest your corpus. You do not run it during the challenge. |
| **Detector** | Runs **YOLO11** on each segment and records object classes, counts, and bbox sidecars. |
| **Reasoner** | Calls **NVIDIA Cosmos3-Reason** to write a searchable natural-language description of the segment. |
| **Embedder** | Calls **NVIDIA Cosmos Embed1** to build text (and visual) vectors for hybrid search. |
| **VastDB writer** | Persists embeddings, reasoning, detections, and metadata as a row in your VastDB collection. |
| **Events (prompt-suggester)** | Periodically scans recent segments and writes suggested search prompts / key events for the UI. |

**Builders challenge note:** your archive is **pre-ingested** (the whole pipeline already ran). You don’t need to upload new chunks or invoke any of these functions for this challenge, and re-ingest is not available.

You don’t need to redeploy this graph for the hackathon — treat it as the engine behind search, dashboard, and suggestions.

---

## What you were given

For your team you already have:


| Piece | What it is |
|-------|------------|
| **Ingest pipeline** | DataEngine graph that pre-ingested your corpus (detect → reason → embed → write VastDB). It is not run during the challenge |
| **UI** | Web app at your `INGRESS_URL` (frontend + backend) |
| **S3 buckets** | Chunks + segments for uploads |
| **VastDB** | Indexed segments, embeddings, detections, reasoning text |
| **This repo in Cursor** | Agent **skills** that know how to call every important API — open this project in Cursor and describe what you want |
| **Source code repo** | Full VSS Blueprint (`vss-blueprint`) — optional reading; the live stack is already up |

```bash
cd /vss-blueprint
```

Cloning the Blueprint is **not a requirement**. The live UI, APIs, and Cursor skills in this repo are enough for a strong demo — search, filters, dashboards, mini-apps on top of the archive. Do not rebuild or redeploy DataEngine ingest functions for the challenge.

Open the UI, log in with your team user, and open **this skills repo** in **Cursor**. Skills are how you move fast against the live APIs.

---

## Video corpus (already indexed)

Your team’s VSS archive is **pre-ingested** with the two sources below. Explore it and build on what is indexed; re-ingest is not available, and uploading is not recommended (short clips only).

**One pipeline, one VastDB index, two sources.** Leave out `camera_id` to search both at once, or set it to stay inside one.

Search filters: `camera_id`, `capture_type`, `location`, plus **object class** from detections. A filter value that does not exist returns zero results with no error, so check values with `retrieval/list-metadata` when a filtered search comes back empty.

### Sources

| Source | `camera_id` | `location` | `capture_type` | What’s indexed |
|--------|-------------|------------|----------------|----------------|
| Formula racing | `f1-01` | `england` | `racing` | **2** races: `f1-academy_race` (about 46 min) and `formula-e_race` (about 50 min) |
| Bundesliga football | `bundesliga-01` | `germany`, or an era such as `germany-2017-26` once the era setup has run | `football` | More than **30** full matches, about 100 min each, seasons 1970-71 to 2026-27 |

Everything is stored as 30 s chunks of 5 s segments. Each segment has a caption, embeddings and object detections.

#### 1. Formula racing — `f1-01`

Two races share one `camera_id`, so tell them apart by file name (`f1-academy_race` or `formula-e_race`). Story: race moments, incidents, sponsors on screen. Try: *“safety car leading the field”*, *“cars in the pit lane”*, *“aerial view of the circuit”*, *“driver in the car.”*

#### 2. Bundesliga football — `bundesliga-01`

Every match shares one `camera_id`, so identify a match by file name (season, competition and teams). Story: the same moment across decades of matches. Try: *“player celebrates a goal”*, *“goalkeeper makes a save”*, *“referee shows a red card”*, *“fans waving scarves in the stands.”*

### Where to start

Don’t try to demo everything at once. Pick one source, prove search → filters → UI, then expand. The ready-made prompts in [`prompts/`](prompts/) cover both: `f1-vss/` for Formula racing and `dfl-archive/` for Bundesliga.

### Example queries

- *“Safety car leading the field”* → `f1-01`
- *“Grandstand crowd”* → `f1-01`
- *“Players shake hands before kickoff”* → `bundesliga-01`
- *“Teams walk out with mascots”* → `bundesliga-01`

---

## Suggested playbook

Write full prompts in Cursor: name what you want, point at your team config, and say what to build. A solid loop is **check what is indexed → ship a thin app on search / videos / dashboard**.

### Example prompts (adapt to your use case)

**1. Check what is indexed**

> Show me what is indexed in my team environment (credentials in `/config/<my-team>.config`): videos, clip counts, and the filter values I can search on.
> Then run basic sanity checks on counts and pipeline health.
> *(Cursor will use skills: `retrieval/dashboard`, `retrieval/list-metadata`, `retrieval/login`)*

**2. Race moments board**

> Build a small webpage that searches both races for a moment I type, for example *“safety car leading the field”*.
> Group hits by race (from the file name) and play each hit’s 5 second clip.
> Deploy it **on Kubernetes** (not local) to my team namespace without Docker build/push — Ingress path `/app` on my team host.
> *(Cursor will use skills: `retrieval/login`, `retrieval/search`, `retrieval/videos`, `retrieval/list-metadata`, `deployment/deploy-app-no-registry`)*

**3. Football moments across seasons**

> Build a standalone page that searches the Bundesliga matches for a moment, for example *“player celebrates a goal”*,
> and groups the hits by season, oldest first. Each hit shows the match and plays its clip.
> Filter by `camera_id`. Deploy on K8s at `/app` (or save under `tools/` while iterating), then report the top findings.
> *(Cursor will use skills: `retrieval/login`, `retrieval/search`, `retrieval/videos`, `deployment/deploy-app-no-registry`)*

---

## Rules of the road

- Stay in **your** team credentials, buckets, and UI. Don’t poke other teams’ namespaces.
- Prefer **Cursor + skills** over hand-copying curl forever — but reading a skill once to understand the API is encouraged.
- Don’t burn the whole hackathon redeploying infrastructure; the stack is already up.
- If search returns nothing: check login, check dashboard/pipeline alignment, then check that metadata filter values actually exist (`retrieval/list-metadata`).
- Have fun — the win is a crisp story: *problem → video archive (one of the packs) → search/filters across cameras → insight or action*.