---
name: retrieval-search
description: >-
  Run semantic/hybrid search over the VSS archive via POST /api/v1/search with tags,
  time_filter, metadata_filters, similarity threshold, and LLM synthesis. Use to find
  video moments matching a natural-language query, optionally scoped by location, camera,
  tags, or time.
---

# Retrieval: search (vss2)

Hybrid search (caption text + visual embeddings) over `vss-collection`, ACL-filtered to the caller, with optional LLM synthesis of the top chunks. Requires a JWT (`retrieval/login`).

## Request — `POST /api/v1/search`

```bash
curl -s -X POST "$BACKEND/api/v1/search" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{
    "query": "forklift near loading dock",
    "top_k": 15,
    "llm_top_n": 3,
    "min_similarity": 0.3,
    "tags": ["warehouse"],
    "time_filter": "24h",
    "metadata_filters": {"location": "Warehouse A", "camera_id": "CAM-001"},
    "include_public": true
  }'
```

| Field | Default | Notes |
|-------|---------|-------|
| `query` | — | required natural-language text |
| `top_k` | 15 | rows returned (1–100) |
| `llm_top_n` | 3 | top chunks sent to the LLM synthesizer; minimum **1** (422 below that) — synthesis cannot be turned off |
| `min_similarity` | 0.1 | does not act as a cutoff on the returned `similarity_score` — do not rely on it to hide weak hits; see "Filtering by score" below |
| `tags` | `[]` | tag filter |
| `time_filter` | `all` | `5m`/`15m`/`1h`/`24h`/`7d`/`custom`; a relative window (`24h`, `7d`) returns nothing if the footage is older than the window |
| `custom_start_date`/`custom_end_date` | — | ISO 8601, with `time_filter:"custom"` |
| `metadata_filters` | `{}` | dict of column→value (e.g. `location`, `camera_id`, `capture_type`); an unknown key 500s — resolve valid keys via `/metadata/schema` first |
| `include_public` / `public_only` | true / false | scope |
| `hybrid_text_weight` | backend default | caption vs visual blend (0–1) |
| `system_prompt` | — | override the synthesis system prompt |

## Filtering by score

`min_similarity` does not filter the response — apply the cutoff yourself on each
result's `similarity_score`. Start at about 0.35 and make it adjustable; good hits on
this footage score roughly 0.35-0.55, and if there is a clear gap in the scores, cut at
the gap instead. If nothing passes the cutoff, that is a valid answer, not an error:
show a clear "no good matches" state. Optionally offer the top few results below the
cutoff, labelled as weak matches, or let the user lower the cutoff — don't silently
drop the cutoff to fill the page, and don't present weak hits as good ones.

## Latency

A search with hits usually takes about 5-10 s and can take about twice that, depending
on the footage being searched and on load. Most of the time is the model writing
`llm_synthesis`. A call that takes 15-20 s is not hung; use a client timeout of at
least 60 s.

Asking for a shorter summary with `system_prompt` usually makes it faster, but not on
every call:

    "system_prompt": "Answer in one short sentence. No lists."

The hits returned are the same; only the summary is shorter. Lowering `llm_top_n` does
not speed it up.

## Building filters (do it client-side)

There is **no** `/tags` or `/locations` route. Discover valid `metadata_filters` keys/values from `retrieval/list-metadata` (`/metadata/schema`, `/metadata/values?field=`). Parse the user's phrasing ("last hour", "in Midtown", "traffic cameras") into `time_filter` + `metadata_filters` + `tags` yourself, then pass the cleaned natural-language remainder as `query`.

## Response

- `results[]` — segment hits (`source`, `similarity_score`, `reasoning_content`, timing…).
- `chunk_results[]` — hits grouped by parent upload (jump-to-moment): `original_video`, `best_match_start_sec/end_sec`, `preview_source`, `matched_segment_count`.
- `llm_synthesis` — `{response, segments_used, model, tokens_used, ...}` (only if hits found).
- `sql_query` — the VastDB query executed (debug).

Play a hit with `retrieval/videos` (`/videos/stream?source=…`). For a grounded natural-language answer instead of raw hits, use `retrieval/agent-qa`.

## Related surfaces

- `POST /api/v1/tools/search` — same engine, agent-tool tag.
- `POST /api/v1/agent/search-and-answer` — same request body, returns an answer + chunk evidence (`retrieval/agent-qa`).

## Agent instructions

1. Ensure a JWT.
2. Split the user's ask into `query` + `time_filter` + `metadata_filters` + `tags`; verify filter fields via `list-metadata`.
3. Filter weak hits yourself on `similarity_score` (see "Filtering by score"), not via `min_similarity`; use `chunk_results` for "which video", `results` for "which exact moment".
4. Cite `llm_synthesis.response` when present; otherwise summarize `chunk_results`.
