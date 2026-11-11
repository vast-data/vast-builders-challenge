# Vast Database (vss2)

Raw access to the team’s VastDB with the `vastdb` Python SDK — **not** the JWT retrieval API.

Connect to the **data VIP** from `S3_ENDPOINT` in `/config/<team>.config`. Reads may optionally use the Query Engine VIP from the backend K8s secret. Writes always use the data VIP.

## Skills

| Skill | Purpose |
|-------|---------|
| [vastdb-read](vastdb-read/SKILL.md) | Catalog + select (data VIP / optional QE) |
| [vastdb-write](vastdb-write/SKILL.md) | Create schema/table + insert (data VIP only) |

## Prerequisites: Python + vastdb

The VM only has `/usr/bin/python3` — no `python`, no pip, no ensurepip (`python3-venv` isn't
installed), and no `vastdb` / `pyarrow` / `pyyaml`. Set this up yourself; don't ask the user
and don't use `sudo` or `apt`.

**1. Check first** — skip the rest if this succeeds:

```bash
python3 -c "import vastdb, pyarrow, yaml"
```

**2. If it fails, create a user-space venv.** A plain `python3 -m venv` fails on this image
because `ensurepip` is missing, so build it without pip and bootstrap pip inside it:

```bash
python3 -m venv --without-pip ~/vastdb-venv
curl -sS https://bootstrap.pypa.io/get-pip.py | ~/vastdb-venv/bin/python -
~/vastdb-venv/bin/pip install vastdb pyarrow pyyaml
```

No sudo, no system packages touched, no `python` alias needed. This is a one-time step per
VM — once the venv exists, step 1's check will pass.

**3. Run the skill scripts with the venv interpreter explicitly** — an agent's shell may not
keep an activated venv between commands, so don't rely on `source .../activate`. Resolve the
interpreter once and reuse it:

```bash
PY=~/vastdb-venv/bin/python; [ -x "$PY" ] || PY=python3
"$PY" .cursor/skills/vast-database/vastdb-read/list_catalog.py
```

Use `"$PY"` in place of a bare `python`/`python3` in every example below.
