---
name: vast-database-football-eras
description: >-
  One-time setup for the Bundesliga track. Labels every football clip in the search
  table with its era (five eras) in the location field, so a search can be limited to
  one era and runs faster. Run it before building a Bundesliga app. It is
  the only permitted write to the search table. Safe to run again.
---

# Vast Database: football eras (setup)

All football clips share one `camera_id`, so a football search scores the whole football
archive. This setup writes each clip's **era** into its `location` field, so a search can
be limited to one era and is faster.

## What it changes

- **One field, `location`**, on rows whose `camera_id` is `bundesliga-01`.
- Before: every football clip has `location = germany`. After: one of the five values
  below.

| `location` value | Seasons |
|------------------|---------|
| `germany-1970-84` | up to 1984-85 |
| `germany-1985-97` | 1985-86 to 1999-00 |
| `germany-2000-09` | 2000-01 to 2009-10 |
| `germany-2010-16` | 2010-11 to 2016-17 |
| `germany-2017-26` | 2017-18 onward |

A season belongs to the era of its first year, and all clips of a match stay together.

## The one exception to the no-write rule

Other skills say never to write to `vss-collection`. This script is the only exception:
it is a setup step, it writes only the `location` field, and it checks its own result.
Run the script as it is. Do not write your own update against the search table, and do
not extend this one to other fields.

## Run it

See [vast-database/README.md](../README.md#prerequisites-python--vastdb) for Python setup
and resolve `$PY` first. The script reads the team config from `/config/<team>.config`.

```bash
PY=~/vastdb-venv/bin/python; [ -x "$PY" ] || PY=python3
"$PY" .cursor/skills/vast-database/football-eras/label_eras.py status   # read-only
"$PY" .cursor/skills/vast-database/football-eras/label_eras.py apply    # the setup step
```

- `status` changes nothing. It prints how many football clips carry each value and
  whether the eras are applied.
- `apply` labels every football clip, then reads the table back and prints `OK` when
  every clip has its era. Rows that are already right are skipped, so running it again
  is harmless.
- If it prints `Stopping: ...`, nothing was changed. Report the message; do not work
  around it.

## Use the eras in a search

Add the era to `metadata_filters`, next to the camera:

```json
{"camera_id": "bundesliga-01", "location": "germany-2017-26"}
```

- A value that does not exist returns zero hits with no error. If an era search comes
  back empty on a stack where the setup was never run, `status` will say "not applied".
- After the setup, `location = germany` no longer matches any clip.

How an app should offer the eras to its user is in the Bundesliga context prompt
(`prompts/dfl-archive/00-foundation.md`).

## Agent instructions

1. Run `status` first. If the eras are already applied, do not run `apply` again.
2. Run `apply` once, as a setup step, before building a Bundesliga app. Tell the user
   in one line what it did (clips relabelled, and that only the `location` label changed).
3. Never write to the search table in any other way, and never print credentials.
