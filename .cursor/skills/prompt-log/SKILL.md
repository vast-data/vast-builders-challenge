---
name: prompt-log
description: >-
  Append the user's own prompt, verbatim and with credentials redacted, to this
  desktop's prompt log file before acting on it. Triggered every turn by the
  always-apply rule in .cursor/rules/build-day.mdc — don't wait for the user to ask,
  and don't skip turns. Gives the team a reproducible, judgeable record of what was
  actually asked, included in the repo they submit.
---

# Prompt log

A running, append-only transcript of what the team actually typed to Cursor, written to
the repo so it travels with the submission. Not a summary, not a cleaned-up version —
the literal prompt, minus anything that looks like a credential.

## Why per-desktop, not one shared file

Two teammates on the same team get **separate VMs** (one each), so they have **separate
clones of this repo** — nothing syncs between them until someone explicitly pushes and
the other pulls. A single shared `PROMPT_LOG.md` that both desktops append to would
collide: both sides add lines at the end of the same file, and a later merge turns that
into a conflict to resolve by hand, every time, exactly the failure mode discussed when
this came up for any other shared-state idea.

So each desktop logs to its own file, named for its own host, and nobody has to merge
anything to avoid a collision:

```
prompt-logs/<hostname>.md
```

Get `<hostname>` once per session with `hostname`. If two teammates end up with the same
value (unlikely, but possible on identical VM images), add a short disambiguator — the
team number plus a random 4-char suffix picked once and reused for the rest of the
session is fine; don't regenerate it every turn.

If the team wants a single combined view later, that's a manual step for them (cat both
files together, or merge one into the other) — this skill never does it automatically,
and never force-merges or deletes either teammate's file.

## What to log

- **Every user message**, in the order it arrived, including short ones ("yes", "try
  again") — the point is reproducibility, not a curated highlight reel.
- **The user's own text only.** Never log your own responses, tool output, file
  contents, or command output. Those aren't the user's prompt, and tool output is a much
  likelier place for a real secret to leak than something a person typed.
- Append **before** acting on the request, not after, so the record survives even if the
  turn errors out or the session ends mid-task.

## Redaction (do this before writing anything)

Replace with `[REDACTED: credential]` — keep the rest of the message intact around it:

- The literal value of anything documented in `config.example`
  (`PASSWORD`, `ACCESS_KEY`, `SECRET_KEY`, `WANDB_API_KEY`, or any other value from
  there), if a user ever pastes one in directly.
- Anything shaped like a bearer token, API key, or password: long hex/base64-looking
  strings, `Bearer <...>`, `AKIA...`, `key=`, `password=`, `token=`, or similar, whether
  or not it matches a known variable.
- A full URL that embeds credentials (`https://user:pass@host/...`) — redact the
  `user:pass@` part only, keep the rest of the URL.

When in doubt, redact. Losing a little color from the log is fine; leaking a credential
into a file that gets pushed to a public submission repo is not.

## Format

Append one entry per user turn to `prompt-logs/<hostname>.md`. Create the file with a
one-line header if it doesn't exist yet:

```markdown
# Prompt log — <hostname>

Raw prompts from this desktop, in order, credentials redacted. Appended automatically;
see .cursor/skills/prompt-log/SKILL.md.
```

Then one block per turn:

```markdown
## <ISO 8601 timestamp>

<the user's prompt, verbatim, redacted as above>
```

Use a plain `## timestamp` heading per entry, not a numbered list — it keeps diffs
append-only (each entry is new lines at the end, nothing upstream changes).

## What this skill does not do

- Never commits or pushes the log file. It just keeps it current in the working tree;
  whether and when it's committed is up to the team's normal git workflow.
- Never edits or reorders past entries, even to fix a typo in an old one — append-only,
  always.
- Never logs anything if the only thing to log is empty or purely a tool-result
  continuation with no new user text (e.g. an automated retry) — there has to be an
  actual user message.
