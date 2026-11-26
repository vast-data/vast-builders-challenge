---
name: retrieval-videos
description: >-
  Browse, play, and summarize indexed videos via /api/v1/videos/* — explore (timeline),
  stream and playback-url (playback), detections (YOLO bbox), metadata (segment row), and
  POST /videos/synthesize (LLM summary/report over a whole parent video). Use to list,
  play back, inspect, or summarize a specific video.
---

# Retrieval: videos (vss2)

Playback + per-video inspection + on-demand summarization. All JWT (`retrieval/login`). `original_video` = parent upload S3 URI; `source` = a single segment clip S3 URI.

## Browse — `GET /api/v1/videos/explore`

Lists **fully-indexed** parent chunks (no query needed).

```bash
curl -s "$BACKEND/api/v1/videos/explore?scope=all&limit=48&offset=0" -H "Authorization: Bearer $TOKEN"
# optional: &date=YYYY-MM-DD &location=<label>
```

`limit` maxes out at 100 — above that the request 422s. Take `source` / `original_video` for
the calls below from what `explore` (or a search) returns, not from a guessed key.

Each chunk's top-level `reasoning_content` is only the **first 5 s segment's** caption.
Per-segment captions, sources and start times are in `chunks[].timeline[]`, one entry
per 5 s segment, each with its own `reasoning_content`, `source` and start time — read
`timeline[]` to get every segment's caption; reading only the chunk-level field
undercounts about six-fold (30 s chunk / 5 s segments).

## Play — `GET /api/v1/videos/stream` / `playback-url`

JWT goes in `?token=` (not a header). Call these from server code only; for an app, see
"Serving clips from an app" below.

```bash
# Range-capable proxy stream (seekable):
"$BACKEND/api/v1/videos/stream?source=s3://$S3_SEGMENTS_BUCKET/<key>&token=$TOKEN"
# Or a presigned S3 GET URL (needs bucket CORS for direct browser playback):
curl -s "$BACKEND/api/v1/videos/playback-url?source=s3://$S3_SEGMENTS_BUCKET/<key>&token=$TOKEN&expires_in=3600"
```

Passing a chunk's `original_video` as `source` instead of a segment's returns the whole
~30 s chunk file (roughly 8-16 MB, depending on the footage) — this is how to fetch a full chunk
rather than one 5 s segment.

## Serving clips from an app

`/videos/stream` answers with `Content-Type: binary/octet-stream`, and its URL carries
the JWT, so do not point a `<video>` tag at it. Give the app a small server-side route
(for example `clip?source=...`) that calls `/videos/stream` with the token, forwards
the browser's `Range` header, returns the upstream status (200 or 206) with
`Content-Range`, `Accept-Ranges` and `Content-Length`, and sets
`Content-Type: video/mp4`. The `<video>` tag points at that route.

## Inspect a segment

```bash
curl -s "$BACKEND/api/v1/videos/metadata?source=s3://$S3_SEGMENTS_BUCKET/<key>" -H "Authorization: Bearer $TOKEN"    # row: reasoning, tags, timing
curl -s "$BACKEND/api/v1/videos/detections?source=s3://$S3_SEGMENTS_BUCKET/<key>" -H "Authorization: Bearer $TOKEN"  # YOLO bbox sidecar JSON
```

`source` is a team-prefixed S3 URI. Take the real `source` from an `explore` or `search`
result rather than building one.

`detections` 404 = no YOLO sidecar for that segment (detector disabled or no detections).

## Summarize / report — `POST /api/v1/videos/synthesize`

LLM summary over **all** segments of one parent video (no VastDB write). This is the "generate a report/summary for this video" capability (there is no `/reports` route).

```bash
curl -s -X POST "$BACKEND/api/v1/videos/synthesize" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{
    "original_video": "<original_video from explore or search>",
    "question": "Summarize what happens in this video",
    "max_segments": 40
  }'
```

Optional `system_prompt` overrides the default (chronological Overview + Timeline markdown). Response: `answer`, `llm_synthesis`, `segment_count`, `segments_used`, `generated_at`. 404 if no accessible segments. Take `original_video` from an `explore` or `search` result, not a guessed key — the bucket is team-prefixed.

## Related

Most of these are also exposed as agent tools under `/api/v1/tools/*` (`segments`, `segment`, `synthesize`, `detections`); `tools/explore` returns 500 on this stack — see `retrieval/agent-qa`.

## Agent instructions

1. Ensure a JWT; use `explore`/`search` to get `original_video`/`source` URIs first.
2. Playback endpoints take the token as `?token=`; all others use the header.
3. For "summarize/report on this video" → `POST /videos/synthesize` (whole parent); for a specific question → `retrieval/agent-qa`.
