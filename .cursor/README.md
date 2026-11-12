# VSS2 Cursor Skills

Agent skills for working with the VSS2 video search stack. Each skill lives in its own folder with a `SKILL.md` that has full usage instructions — open that file when you need details.

## Layout

```
.cursor/skills/
├── deployment/             # Deploy retrieval K8s apps + hackathon mini-apps
├── ingest/                 # Upload new video or re-ingest indexed archive
├── retrieval/              # Query and explore indexed video
└── vast-database/          # Raw VastDB SDK read/write (not the JWT API)
```

Runtime configuration is mounted outside the repo at absolute `/config/`:

- `/config/<team>.config` — team credentials. Models are reached only through the pipeline API; there's no direct model access or GPU bearer here.
- `/config/${USERNAME}-k8s.yaml` — Kubernetes access, named after the team's `USERNAME` (e.g. `/config/<username>-k8s.yaml`)
- `/config/backend-secret.yaml` — retrieval backend secret (and `/config/vss-cli-secret.yaml` when aligning ingest keys)

Skills must not search the repo's `team-configs/`.

## Ingest

**Re-ingest** for content already in the team archive (hackathon default). **Upload**
when adding a new local video via the backend (`POST /api/v1/videos/upload`).

| Skill | Summary |
|-------|---------|
| [upload-video](skills/ingest/upload-video/SKILL.md) | Multipart upload of a new video via backend upload API |
| [reingest-videos](skills/ingest/reingest-videos/SKILL.md) | Re-ingest a selected indexed video/stream via dashboard API |
| [reingest-chunk](skills/ingest/reingest-chunk/SKILL.md) | Re-ingest one specific Explore card / chunk |

→ [ingest/README.md](skills/ingest/README.md)

## Retrieval

Query the indexed archive through the backend API (`/api/v1`). Most routes need a JWT — start with **login**.

| Skill | Summary |
|-------|---------|
| [login](skills/retrieval/login/SKILL.md) | Authenticate and obtain a bearer token |
| [search](skills/retrieval/search/SKILL.md) | Semantic/hybrid search over the archive |
| [list-metadata](skills/retrieval/list-metadata/SKILL.md) | Discover filterable fields and values |
| [dashboard](skills/retrieval/dashboard/SKILL.md) | Aggregate stats and ingest health |
| [suggest-prompts](skills/retrieval/suggest-prompts/SKILL.md) | AI-generated search prompt suggestions |
| [videos](skills/retrieval/videos/SKILL.md) | Browse, play back, and summarize a video |
| [agent-qa](skills/retrieval/agent-qa/SKILL.md) | Natural-language Q&A over the archive |

→ [retrieval/README.md](skills/retrieval/README.md)

## Vast Database

Raw SDK access to the team’s VastDB bucket (bypasses the JWT API).

| Skill | Summary |
|-------|---------|
| [vastdb-read](skills/vast-database/vastdb-read/SKILL.md) | Raw VastDB catalog + select (data VIP / optional QE) |
| [vastdb-write](skills/vast-database/vastdb-write/SKILL.md) | Create schemas/tables + insert (data VIP only) |

→ [vast-database/README.md](skills/vast-database/README.md)

## Deployment

Retrieval-side Kubernetes apps (`deployments/vss-k8s-application/` in the blueprint tree).

| Skill | Summary |
|-------|---------|
| [build-yamls](skills/deployment/build-yamls/SKILL.md) | Fill secrets + namespace/cluster/image tags |
| [deploy](skills/deployment/deploy/SKILL.md) | Build/push + quick deploy + ingress |
| [health](skills/deployment/health/SKILL.md) | Pods, `/health`, `/api/v1/config` |
| [deploy-app-no-registry](skills/deployment/deploy-app-no-registry/SKILL.md) | On-cluster mini-app at `/app` on the team host (no Docker/registry) |

→ [deployment/README.md](skills/deployment/README.md)

## Typical flows

**Upload a new file** → `login` → `upload-video` → `dashboard` / `videos`

**Re-ingest** → `login` → `reingest-videos` (or `reingest-chunk`) → `dashboard`

**Search** → `login` → `list-metadata` (optional) → `search` or `agent-qa`

**Watch a result** → `login` → `videos`

**VastDB custom tables** → `vast-database/vastdb-write` (create/insert on data VIP) → `vast-database/vastdb-read` (select)

**Hackathon mini-app (no Docker)** → write small app → `deployment/deploy-app-no-registry` → open `https://team-<N>-app.thecosmoslabs.com/app/` (`$APP_URL`, `<N>` = team number)
