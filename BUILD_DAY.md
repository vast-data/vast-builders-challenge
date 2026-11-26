# VAST Builders Corner: Build Day Guide

The infrastructure is already running, so you skip straight to the interesting part: turning hours of video into something that searches, reasons, and acts.

## 1. Kickoff

### What you're building
An app that understands video and does something with it. Search hours of
footage in plain language, ask what happened, detect and track objects, or call an action
when something matters. 

**Pick one idea and build a working app.**

## 2. Skills, Skills, Skills

The core skills are in `retrieval/`, under `.cursor/skills/`. More
skills cover the rest of the deployed stack, if you want to explore. Each skill guides the
coding agent: the endpoint, the request, the response, and what to do when it fails.

Describe what you want and the coding agent loads the matching skill.

```
"show me what footage is indexed"
"find the safety car leading the field"
"summarize what happens in the first ten minutes of the race"
```

Skills read what they need from environment variables, so nothing should ask you for a
password or a URL. If something isn't working, ask for help.

### Find what's missing

Search for something your idea needs that the existing descriptions probably don't mention.
Counts of people. What someone is carrying. Whether a vehicle stopped.

If it comes back empty, that's not a broken search. It means the ingestion prompt never
asked about it, so nothing was written down.

### Build on what's indexed

The video is already indexed, and the descriptions are fixed: re-ingest is not available
on this stack, and uploading new video is not recommended. Read a few captions for your footage before you settle on
an idea, and pick one the captions can support.

> 💡 That gap, between what you searched for and what the prompt asked about, is the thing
> to keep in mind. Everything you can build depends on what the descriptions say.

### Retrieval: Searching Video

| Skill | Use it to |
|-------|-----------|
| `search` | Find moments matching a description, with filters for time, location, camera, tags. |
| `agent-qa` | Ask a question and get an answer with evidence, instead of a list of hits. |
| `videos` | Browse what's indexed, play a clip, read its captions and detections, summarize a whole video. |
| `dashboard` | Check what's indexed and whether ingest is healthy. |
| `suggest-prompts` | Get generated example queries and notable recent events. |

## 3. Build

### What "done" looks like
You have a working index and you know how to query it. What comes next is what you
build on top. A small app, agent, or a dashboard. A clear use case.

### What video you have

The videos come from two kinds of real-world footage:

- Formula racing footage (F1 Academy and Formula E)
- Bundesliga football footage

Explore what's actually indexed in the [Video Search & Summary UI](README.md#2-video-search--summary-ui-demo-app).

Your index is already full and searchable. For the two demo tracks (Formula racing,
camera_id f1-01; Bundesliga, camera_id bundesliga-01) see "What to know about the footage"
in [prompts/README.md](prompts/README.md).

### The loop

1. **Pick a use case**
2. **Build an app or agent**
3. **Deploy and iterate**

> 💡 Once you've deployed with `/deploy-app-no-registry`, check out your app in your own
> browser at [workshop.thecosmoslabs.com](https://workshop.thecosmoslabs.com) — click **App**.

<p align="center"><img src="docs/images/view-deployed-app.png" alt="The App button on the VAST workshop home page, for viewing your deployed app" width="90%"></p>

Check that the existing captions cover what your idea needs before you build on them. If
they don't, adjust the idea: the footage can't be re-indexed on this stack.

### LLM access

Search and Q&A come from your VSS instance. Anything your app decides on top of that,
classifying results, drafting a summary, choosing an action, runs on <a href="https://docs.wandb.ai/inference" target="_blank" rel="noopener">serverless LLM inference from Weights & Biases</a>.

Your `WANDB_` keys are already in your environment. Point
your own app's reasoning or agent at the inference endpoint using those. If you need more
credits, reach out to the Weights & Biases by CoreWeave team :)

The skills used by Cursor can be used by agent frameworks too. They follow the standard
`SKILL.md` format, so most frameworks load them straight from `.cursor/skills/`.

## Reference

### Health check

If something isn't working, pull first. The repo is pre-cloned and may be behind. Type
the following into Cursor:

```
run a git pull
```

Then ask Cursor:

```
check that everything is working
```

If it fails, or you need more help, run `/ask-help`. The skill writes a note with the relevant details but **does not post it**. Copy it and share it with an organizer, and we'll debug it together.

### Architecture Reference

For the full video corpus, metadata reference, and example queries, see the [Architecture Reference](ARCHITECTURE_REFERENCE.md).

### More prompts

For more prompts on the formula racing and football tracks, see [`prompts/`](prompts/).
