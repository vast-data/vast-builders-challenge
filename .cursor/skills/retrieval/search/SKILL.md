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
    "query": "safety car leading the field",
    "top_k": 15,
    "metadata_filters": {"camera_id": "f1-01"},
    "system_prompt": "Reply with only the word OK."
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
result's `similarity_score`. Start at the default the track's context prompt gives (0.30 for
Formula racing, 0.35 for Bundesliga) and make it adjustable. If nothing passes the cutoff, that is a valid answer, not an error:
show a clear "no good matches" state. Optionally offer the top few results below the
cutoff, labelled as weak matches, or let the user lower the cutoff — don't silently
drop the cutoff to fill the page, and don't present weak hits as good ones.

## Latency

A search with hits can take several seconds, and longer on a large archive or under
load. Most of that is the model writing `llm_synthesis`. Use a client timeout of at
least 60 s, and do not treat a slow call as hung.

A UI that calls search should never show a blank page or a bare spinner for that long:
draw the results layout as a loading skeleton right away, with a short neutral status
line (no numbers), and swap it for real results when they arrive. Have the page call your app's own search route in the background (the
browser never calls VSS directly), do not hold up drawing the page for a search, and
handle the empty and error cases. No timers, countdowns or durations in the UI.

If the app only needs the hits (a list, a timeline, a clip picker), tell the model to
write almost nothing and ignore `llm_synthesis`:

    "system_prompt": "Reply with only the word OK."

The hits are the same and the call is faster. An exact-match filter that selects fewer
clips also shortens a search: the Bundesliga era label is one (see
`vast-database-football-eras`).

Lowering `llm_top_n` does not speed it up.

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
4. Cite `llm_synthesis.response` when you asked for a summary. If you sent the one-word `system_prompt`, ignore `llm_synthesis` and summarize `chunk_results` yourself.
