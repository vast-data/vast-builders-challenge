---
name: build-day-quickstart
description: >-
  Walk someone through the README quickstart step by step: look at the index, ask a
  question, try a starter search on each video track, then pick a prompt from
  `prompts/` to build. Pauses after each step instead of dumping the whole guide.
  Use when someone says they're ready to start, asks "what's next", or wants a guided
  run instead of reading `README.md` themselves.
---

# Build Day Quickstart

This is `README.md`, run interactively. One step at a time, and wait for them before
moving on.

## Step 1: Video Search & Summary UI

Point them to the Video Search & Summary UI on the workshop home page and tell them to
open it in their own browser. Have them try one of the suggested searches and look at
one result: the clip, the timestamp, and the description Cosmos Reason wrote for it.
This is the same API the skills call. The point is to see what is indexed before
touching Cursor.

## Step 2: Look and ask

Run these two in the agent panel, one at a time:

1. `what's in the index? show me a few examples`. They get back ranked segments with
   timestamps and descriptions. Have them play one.
2. `what happens in the first video you showed me? summarize it in three sentences`.
   Point out the difference: the first returns moments, the second reads those moments
   and writes an answer.

## Step 3: Try a use case

Two tracks are indexed: Formula racing and Bundesliga football. Have them run one:

- `show me aerial views of the circuit`
- `show me players celebrating a goal`

Search always returns a full set of results, even weak ones, so ask them to play the
top few and judge whether they match. Do not treat a loose match as proof. A caption
can name something that is not on screen.

## Step 4: Pick a prompt to build

Show the tracks in `prompts/` and let them pick one. Run the track's `00` context
prompt first (it builds nothing), then the demo they chose. Each demo builds its own
small app with suggested searches, and shows its results in the app, not in files.

Remind them once: web app only. Uploads are disabled, and re-ingest is limited to 30
seconds and 3 chunks per request, so build on the footage that is already indexed.

From here they build. Do not keep narrating. Answer what comes up.

## Agent instructions

1. Go one step at a time. After each step, ask if it worked before moving on.
2. If a search comes back empty or something fails, run the health check
   (`retrieval-login` and `retrieval-dashboard`). If that is also unhealthy, hand off to
   `ask-cosmos` instead of troubleshooting further.
3. Use the provided skills for every platform call. Do not write raw REST calls.
4. For more depth, point them to `BUILD_DAY.md`.
