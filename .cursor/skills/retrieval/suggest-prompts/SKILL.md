---
name: retrieval-suggest-prompts
description: >-
  Fetch AI-generated search prompt chips and key events via GET /api/v1/suggestions,
  produced by the prompt-suggester enrichment job from recent VastDB segments. Use to
  seed the search box with relevant example queries or surface notable recent events.
---

# Retrieval: suggest prompts (vss2)

Returns the latest batch of **search prompt suggestions** + **key events** the enrichment `prompt-suggester` computed from recent segments and wrote to VastDB (the `VDB_PROMPTS_COLLECTION` table). Requires a JWT (`retrieval/login`).

## Starter queries

Offer these first — no API call needed, nobody waits. Every one was run against the live
stack and returned relevant hits. They're a fixed starting set; `/suggestions` below gives
generated ones for the current archive.

Formula racing (`metadata_filters: {"camera_id": "f1-01"}`):
`safety car leading the field`, `Red Bull logo`, `Crypto.com logo`, `Hard Rock logo`,
`Nissan logo`, `grandstand crowd`.

Bundesliga football (`metadata_filters: {"camera_id": "bundesliga-01"}`):
`Red jersey player runs with ball toward goal`, `Crowded stadium with red and white fans
waving`, `goal celebration`, `handshakes`, `mascots`, `scarves`.

## Request — `GET /api/v1/suggestions`

This call has taken **about 110–117s** and returned **about 2.5 MB** on every run observed
so far (it's regenerated each time, not cached) — too slow to block a conversation or an
app's page load on. Start it in the background, keep going with the starter queries above,
and use the result when it arrives. Call it at most once per session and reuse the saved
response; only wait on it synchronously if the user explicitly asks for generated
suggestions right now, and tell them it takes about two minutes.

```bash
curl -s --max-time 180 "$BACKEND/api/v1/suggestions" -H "Authorization: Bearer $TOKEN" -o /tmp/suggestions.json &
```

The file is ready to read once that background job finishes.

Content is ACL-filtered to the caller. Use the returned prompts as ready-to-run `query` strings for `retrieval/search`, and key events as highlights.

## Depends on the enrichment pipeline

These come from the scheduled `prompt-suggester` enrichment job writing to the prompts table. If empty:
- The enrichment job may not have run yet.
- Lookback window found no new segments — logs show `[SUGGEST] No new videos in lookback window`.
- Check `retrieval/dashboard` that segments are actually being indexed.

## Agent instructions

1. Ensure a JWT.
2. Treat items as suggestions, not guarantees — feed prompts into `retrieval/search`.
3. If empty, check recent ingest (`retrieval/dashboard`) before assuming a bug.
