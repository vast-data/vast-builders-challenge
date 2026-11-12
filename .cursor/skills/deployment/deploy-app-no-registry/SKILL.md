---
name: deploy-app-no-registry
description: >-
  Deploy a custom hackathon app on top of VSS onto Kubernetes (not local) in the
  team's namespace without Docker build/push — public image (python:3.12-slim),
  app code from a ConfigMap, VSS credentials from a Secret, exposed via Ingress
  at path /app on the team's existing host. Tell users to open the public URL
  https://team-<N>-app.thecosmoslabs.com/app/ (Cloudflare Access may ask them to
  sign in first).
  Use when participants want a mini-app / ops board / API on their archive but
  the VM has no Docker or registry access.
---

# Deployment: custom app without registry (hackathon)

Hackathon VMs typically **cannot build or push images**. Deploy a small app **on
the Kubernetes cluster** (never “run it locally” as the deliverable) by:

1. Running a **public** image (`python:3.12-slim`)
2. Mounting **app code** from a ConfigMap
3. Mounting **VSS credentials** from a Secret (server-side auth to the team's VSS)
4. Exposing it with Deployment + Service + **Ingress path `/app`**

This is **not** a custom-built app image — code is mounted at runtime.

## Non-negotiable: on-cluster + Ingress `/app`

| Rule | Detail |
|------|--------|
| **Must run on K8s** | Deployment in the team's namespace. Do not ship a local Flask/Node server, `python -m http.server`, or “open localhost” as the app. |
| **Must use Ingress** | Path `/app` on the team Ingress host. |
| **One host per team** | Ingress host is the host in `$INGRESS_URL` (the team's existing VSS host). The app shares it; it does not get its own hostname. |
| **Path is `/app`** | Always. Do not invent a new hostname or use `/` (that is the VSS UI). |
| **External URL for humans** | `$APP_URL` = `https://team-<N>-app.thecosmoslabs.com/app/`. Not `$INGRESS_URL`, not `http://$APP_HOST/app` (internal to the lab network, won't load from an attendee's laptop). |

## How to open the app

After deploy, tell the user to open `$APP_URL`
(`https://team-<N>-app.thecosmoslabs.com/app/`). It goes through Cloudflare
Access, so the browser may ask them to sign in first.

Open it **with the trailing slash**, and use relative URLs in the page for the app's
own API calls and assets — without the slash, the page resolves relative URLs one
level up (`/app/api/...` becomes `/api/...`) and its own calls and assets break.
Optionally, have the app redirect a request for the bare path to the slash form.

Do not send them to `$INGRESS_URL` (internal VSS API) or to `http://$APP_HOST/app`
— that host is internal to the lab network and won't load from an attendee's laptop;
it's only for the in-cluster `curl` check in Verify below.

## When to use

- Building a mini-app / ops board / thin API on top of the team's VSS APIs
- No Docker daemon, no registry, or no ability to `docker build`/`push`
- App is small enough to fit in a ConfigMap (soft limit ~1 MiB total)

Do **not** use this for the official retrieval stack (`deploy` / `build-yamls`).
Stay in **your** team namespace only.

## Prerequisites

```bash
mapfile -t TEAM_CONFIGS < <(find /config -maxdepth 1 -type f -name '*.config' | sort)
(( ${#TEAM_CONFIGS[@]} == 1 )) || { echo "expected exactly one /config/*.config"; exit 1; }
TEAM_CONFIG="${TEAM_CONFIGS[0]}"
# Do not `source` on zsh (USERNAME is reserved). Parse keys:
USERNAME=$(grep '^USERNAME=' "$TEAM_CONFIG" | cut -d= -f2-)
INGRESS_URL=$(grep '^INGRESS_URL=' "$TEAM_CONFIG" | cut -d= -f2-)
PASSWORD=$(grep '^PASSWORD=' "$TEAM_CONFIG" | cut -d= -f2-)

# Namespace = this team only (e.g. team-17). Confirm with the user if unclear.
NS="$USERNAME"
export KUBECONFIG=/config/${NS}-k8s.yaml   # e.g. /config/<username>-k8s.yaml
# team account is namespace-scoped; cluster-info returns Forbidden
kubectl -n "$NS" get pods

# Ingress host (cluster, internal). Users open $APP_URL below, not this host.
# The app shares the team's VSS host; take it from INGRESS_URL.
APP_HOST=$(echo "$INGRESS_URL" | sed -E 's#^https?://##; s#/.*$##')

# Public URL people open (through Cloudflare). Team number = trailing digits of USERNAME.
TEAM_N="${USERNAME##*[!0-9]}"
APP_URL="https://team-${TEAM_N}-app.thecosmoslabs.com/app/"
```

`$INGRESS_URL` from `/config/<team>.config` is only for the app's **backend** calls (`VSS_URL`).

The app calls the existing VSS backend at `$INGRESS_URL` (see `retrieval/login`,
`retrieval/search`, etc.) — do not redeploy the VSS stack for a demo app.

## Workflow

```
- [ ] 1. Write app files (keep under ~1 MiB total); routes at / (Ingress strips /app)
- [ ] 2. Create ConfigMap from app code
- [ ] 3. Create Secret from team VSS creds
- [ ] 4. Apply Deployment + Service + Ingress (host=$APP_HOST, path=/app)
- [ ] 5. Verify pod Running + curl http://$APP_HOST/app (in-cluster check; public URL is $APP_URL)
```

### 1. App layout

Keep a small directory, e.g. `tools/my-app/`:

```text
tools/my-app/
├── main.py            # entrypoint (listen on 0.0.0.0:$PORT); routes at /
├── requirements.txt   # optional; pip install at container start
└── ...
```

App reads VSS URL + credentials from env (injected from the Secret), logs in once,
then calls retrieval APIs with the JWT. Prefer `requests` / stdlib; avoid heavy deps.

Serve internally at `/` and `/health`. Ingress rewrites `/app` → `/`.
Users open the app at `$APP_URL` (`https://team-<N>-app.thecosmoslabs.com/app/`)
— not via `$INGRESS_URL` or `http://$APP_HOST/app`.

**ConfigMap limits:** total data ≈ 1 MiB. No large models, videos, or `node_modules`.

### 2. ConfigMap (code)

```bash
APP_DIR=tools/my-app          # adjust
APP_NAME=hackathon-app        # k8s resource prefix; lowercase DNS-1123

kubectl -n "$NS" create configmap "${APP_NAME}-code" \
  --from-file="$APP_DIR" \
  --dry-run=client -o yaml | kubectl apply -f -
```

After code changes: re-run the same `create … | apply`, then restart the Deployment
(ConfigMap updates are **not** picked up by a running pod automatically).

### 3. Secret (VSS credentials)

```bash
kubectl -n "$NS" create secret generic "${APP_NAME}-vss-creds" \
  --from-literal=VSS_URL="$INGRESS_URL" \
  --from-literal=VSS_USERNAME="$USERNAME" \
  --from-literal=VSS_PASSWORD="$PASSWORD" \
  --dry-run=client -o yaml | kubectl apply -f -
```

**No VastDB access from the deployed app.** This Secret only holds `VSS_URL` /
`VSS_USERNAME` / `VSS_PASSWORD`, and `python:3.12-slim` has no `vastdb` package and no
`ffmpeg` — a deployed app can call the VSS API but cannot read or write VastDB tables,
or run binaries that aren't in the base image, as deployed. Three cases:

- **Reading table data:** do the VastDB read from the VM with the `vast-database`
  skills, write the rows it needs to a small JSON file in the app directory, and ship
  that file in the ConfigMap (step 2) — label it in the app as a snapshot with its time.
- **Saving user actions** (an accept/reject set, a licence, a usage event): keep the
  state in the app's memory and add an export endpoint; a VM-side script reads that
  export and writes it to VastDB with the `vast-database` skills, then re-creates the
  ConfigMap with the refreshed snapshot.
- **Features needing a binary** (`ffmpeg`, etc.): run it on the VM, not in the pod, and
  ship its results as a snapshot the same way.

Either way, re-create the ConfigMap and restart the Deployment to refresh the snapshot
(see Update loop below). Keep the snapshot small; the ConfigMap limit is still ~1 MiB
total. Two cautions: in-memory app state is lost on restart and shared by every viewer
of the URL, so export it before refreshing the snapshot; and `--from-file=<dir>` skips
subdirectories, so keep app files flat.

### 4. Deployment + Service + Ingress

Ingress **must** reuse the team's host and path `/app` (nginx rewrite strips the prefix
so the container still sees `/`):

```bash
APP_PORT=8080

kubectl -n "$NS" apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ${APP_NAME}
  labels:
    app: ${APP_NAME}
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ${APP_NAME}
  template:
    metadata:
      labels:
        app: ${APP_NAME}
    spec:
      containers:
      - name: app
        image: python:3.12-slim
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: ${APP_PORT}
        env:
        - name: PORT
          value: "${APP_PORT}"
        - name: VSS_URL
          valueFrom:
            secretKeyRef:
              name: ${APP_NAME}-vss-creds
              key: VSS_URL
        - name: VSS_USERNAME
          valueFrom:
            secretKeyRef:
              name: ${APP_NAME}-vss-creds
              key: VSS_USERNAME
        - name: VSS_PASSWORD
          valueFrom:
            secretKeyRef:
              name: ${APP_NAME}-vss-creds
              key: VSS_PASSWORD
        volumeMounts:
        - name: code
          mountPath: /code
        workingDir: /code
        command: ["bash", "-c"]
        args:
        - |
          set -euo pipefail
          if [ -f requirements.txt ]; then
            pip install --no-cache-dir -q -r requirements.txt
          fi
          exec python main.py
        readinessProbe:
          httpGet:
            path: /health
            port: ${APP_PORT}
          initialDelaySeconds: 10
          periodSeconds: 10
      volumes:
      - name: code
        configMap:
          name: ${APP_NAME}-code
---
apiVersion: v1
kind: Service
metadata:
  name: ${APP_NAME}
  labels:
    app: ${APP_NAME}
spec:
  selector:
    app: ${APP_NAME}
  ports:
  - name: http
    port: 80
    targetPort: ${APP_PORT}
  type: ClusterIP
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ${APP_NAME}
  labels:
    app: ${APP_NAME}
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /\$2
spec:
  ingressClassName: nginx
  rules:
  - host: ${APP_HOST}
    http:
      paths:
      - path: /app(/|$)(.*)
        pathType: ImplementationSpecific
        backend:
          service:
            name: ${APP_NAME}
            port:
              number: 80
EOF
```

Ingress is on `$APP_HOST` path `/app` — that host is internal to the lab network.
Users open `$APP_URL` (`https://team-<N>-app.thecosmoslabs.com/app/`), the public
address that routes through Cloudflare to the same Ingress.

Do **not** create a second hostname for the app. Do **not** use path `/` (conflicts
with the VSS frontend Ingress on the same host).

Other public images are fine when Python is wrong (`node:22-slim`, etc.) — still
**no** custom build/push, still Ingress path `/app`.

### 5. Verify

```bash
kubectl -n "$NS" rollout status deploy/"$APP_NAME"
kubectl -n "$NS" get pods,svc,ingress -l app="$APP_NAME"
kubectl -n "$NS" logs -l app="$APP_NAME" --tail=100

for i in $(seq 1 10); do
  code=$(curl -sS -o /dev/null -w "%{http_code}" "http://${APP_HOST}/app")
  [ "$code" = 200 ] && break
  sleep 3
done
echo "$code"
curl -sS "http://${APP_HOST}/app/health"
```

A 503 in the first few seconds after rollout is normal while the Ingress picks up the
new pod; only a 503 that persists past these retries (~30 s) means something is wrong.
These two `curl`s are an **in-cluster** check from the VM only — that host doesn't load
from an attendee's laptop. Tell the user to open `$APP_URL`
(`https://team-<N>-app.thecosmoslabs.com/app/`) instead; Cloudflare Access may ask them
to sign in first. Do **not** tell them to open `$INGRESS_URL`. If `$APP_URL` fails, fix
the Ingress / pod — do not fall back to a local server.

## Update loop

| Change | Action |
|--------|--------|
| App code | Recreate ConfigMap → `kubectl -n $NS rollout restart deploy/$APP_NAME` |
| Creds / VSS URL | Recreate Secret → rollout restart |
| Manifest (port, probe, image) | `kubectl apply` Deployment/Service/Ingress again |

After `rollout restart`, wait a few seconds or retry a check before trusting it — the
old pod can still answer briefly after `rollout status` returns, so a check made right
after a restart can hit the old pod and show stale data.

## Constraints & pitfalls

| Issue | What to do |
|-------|------------|
| Tempted to run locally | Refuse — deploy to K8s + Ingress `/app` only. |
| New hostname for the app | Wrong — Ingress host is the host in `$INGRESS_URL` (the team's existing VSS host), not a new one. |
| Ingress path `/` or random path | Wrong — path must be `/app`. |
| `ImagePullBackOff` | Cluster must pull Docker Hub; ask organizers if blocked. |
| ConfigMap too large | Trim assets; stay under ~1 MiB. |
| Pod crashes | `kubectl logs`; missing dep or not binding `0.0.0.0`. |
| 401 from VSS | Secret vs `/config/<team>.config`; see `retrieval/login`. |
| `/app` 404 / wrong backend | Check rewrite annotation + path `/app(/|$)(.*)` on this team's host. |
| 503 right after deploy | Wait and retry — Ingress hasn't picked up the new pod yet. |
| Wrong namespace | Only **this** team (`$USERNAME` / confirmed `NS`). |
| App needs VastDB table data | Pod has no VastDB credentials or package. Read the table from the VM and ship a JSON snapshot in the ConfigMap. |
| Page loads but its API calls 404 | Opened without the trailing slash, or the page uses absolute URLs. Use `/app/` and relative URLs. |

## Agent instructions

1. Deliverable is **on-cluster** via Ingress — never a local-only app.
2. Resolve `NS` from `$USERNAME`. Set `$APP_HOST` to the host in `$INGRESS_URL` (the team's existing VSS host) — do not invent a new hostname. Use `$INGRESS_URL` itself only as `VSS_URL` (internal API).
3. Ingress host = `$APP_HOST`, path = `/app` (with nginx rewrite). No other host/path.
4. Generate a small app (`main.py` + optional `requirements.txt`) that authenticates to VSS and implements the use case; keep internal routes at `/`.
5. Apply ConfigMap → Secret → Deployment/Service/Ingress; prove the pod/Ingress is healthy.
6. On code edits: update ConfigMap + `rollout restart`. Do not suggest `docker build`/`push`.
7. Tell the user to open `$APP_URL` (`https://team-<N>-app.thecosmoslabs.com/app/`). That is the external URL — Cloudflare Access may ask them to sign in first. Do not point them at `$INGRESS_URL` or `http://$APP_HOST/app` (internal to the lab network).
