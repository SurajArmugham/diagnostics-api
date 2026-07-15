# JWT Authentication — Operator Guide

How to obtain tokens, understand expiry, manage secrets before pipeline runs,
and use the API after deployment.

---

## 1. How Authentication Works

```
Client
  ↓  POST /token  (username + password, form-encoded)
FastAPI
  ↓  credentials match API_USERNAME / API_PASSWORD ?
Signed JWT  (HS256, JWT_SECRET_KEY, 30 min expiry)
  ↓  Authorization: Bearer <jwt>
Protected Routes
  - POST /diagnostics
  - GET  /audit-history

Open Route (no token — used by Kubernetes probes):
  - GET  /health
```

This is the same pattern the CD pipeline already uses against Infisical
(Universal Auth: clientId/clientSecret → access token → Bearer header) —
here, our API is the token issuer instead of Infisical.

---

## 2. Getting a Token

### Generate a signing key (one time, before first deploy)

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

Store the output as `JWT_SECRET_KEY` in Infisical (see section 4).
Never reuse this value anywhere else.

### Request a token

```bash
# NOTE: form-encoded (-d), NOT JSON. This is the OAuth2 convention
# and what the Swagger "Authorize" button sends.
curl -s -X POST http://localhost:8000/token \
  -d 'username=<API_USERNAME>&password=<API_PASSWORD>'
```

Response:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

Capture it into a shell variable:

```bash
TOKEN=$(curl -s -X POST http://localhost:8000/token \
  -d 'username=<API_USERNAME>&password=<API_PASSWORD>' \
  | python3 -c 'import sys,json; print(json.load(sys.stdin)["access_token"])')
```

---

## 3. The Expiry "Timer"

There is **no server-side timer**. The expiry is a timestamp (`exp` claim)
stamped INSIDE the token when it is issued
(`ACCESS_TOKEN_EXPIRE_MINUTES = 30` in `app/auth/auth_service.py`).
Every request re-checks `exp` against the current clock during
`jwt.decode()`. Kubernetes plays no role in token expiry.

### Inspect a token's claims (including expiry)

```bash
# Decode the payload (middle) segment of the JWT:
echo "$TOKEN" | cut -d. -f2 | base64 -d 2>/dev/null | python3 -m json.tool
```

Output:

```json
{
    "sub": "diagnostics-admin",
    "exp": 1752574800
}
```

Convert `exp` to a human-readable time:

```bash
python3 -c "import datetime; print(datetime.datetime.fromtimestamp(1752574800))"
```

When the token expires the API returns `401 Invalid or expired token` —
simply request a fresh token from `/token`. No state to clean up.

---

## 4. Secret Checklist — BEFORE Running Pipelines

| Store | Keys | When to update |
|---|---|---|
| **Infisical vault** | `API_USERNAME`, `API_PASSWORD`, `JWT_SECRET_KEY` (plus existing `DB_*`, `SSH_*`) | **Before the FIRST Kubernetes CD run** after this change, and on any rotation. CD recreates `diagnostics-secret` from Infisical on every run — missing keys cause pods to fail with `CreateContainerConfigError`. |
| **GitHub secrets** | `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN` (CI push), `INFISICAL_CLIENT_ID`, `INFISICAL_CLIENT_SECRET`, `INFISICAL_PROJECT_ID` (CD) | Already configured — **no new GitHub secrets needed**. The CI test phase uses dummy values injected by `tests/conftest.py`; tests never touch real credentials. |
| **Local `.env` / `k8s/secret.yaml`** | — | **Not needed for the cluster path.** Only add the 3 new keys if running the app locally via `uvicorn` / `docker compose`. Both files stay gitignored. |

### Rotating JWT_SECRET_KEY

1. Update the value in Infisical.
2. Run the Kubernetes CD workflow (recreates the K8s Secret + restarts pods).
3. Effect: ALL outstanding tokens become invalid instantly (their signatures
   no longer verify). Clients just request new tokens. This is the standard
   emergency "log everyone out" lever.

---

## 5. Post-Deployment Usage

### Cluster bring-up (if the cluster was stopped)

```bash
# 1. Start the cluster (Docker Desktop / kind), then verify:
kubectl config current-context
kubectl get nodes

# 2. Apply the TLS secret (local-only file, NOT in Infisical):
kubectl apply -f k8s/tls-secret.yaml

# 3. Start the self-hosted GitHub Actions runner (required for CD —
#    the workflow uses runs-on: self-hosted and will sit in "Queued"
#    forever if no runner is online):
cd ~/github-runner/diagnostics-api-project/actions-runner && ./run.sh
#    Leave it running. Verify it shows "Idle" under:
#    GitHub → repo → Settings → Actions → Runners

# 4. Release flow (GitOps - manifest is the source of truth):
#    a. Push code to main -> CI builds + pushes image :<git-sha>
#    b. Verify the tag on Docker Hub
#    c. Pin <git-sha> in k8s/deployment.yaml (and
#       docker-compose.deploy.yml), commit with "[skip ci]", push
#    d. GitHub -> Actions -> "Kubernetes CD" -> Run workflow
#       (no inputs; single kubectl apply deploys the pinned tag)
#
#    NOTE: "[skip ci]" anywhere in the head commit message skips
#    push-triggered workflows - including in prose! Never write
#    that token in a commit message unless you mean it.
```

### Full verification flow

```bash
kubectl port-forward service/diagnostics-api 8000:8000

# 1. Health is open (Kubernetes probes rely on this):
curl http://localhost:8000/health
# → {"status":"UP"}

# 2. Protected route WITHOUT token → 401:
curl -X POST http://localhost:8000/diagnostics \
  -H 'Content-Type: application/json' \
  -d '{"hostname":"Localhost","service":"sshd"}'
# → {"detail":"Not authenticated"}

# 3. Get a token:
TOKEN=$(curl -s -X POST http://localhost:8000/token \
  -d 'username=<API_USERNAME>&password=<API_PASSWORD>' \
  | python3 -c 'import sys,json; print(json.load(sys.stdin)["access_token"])')

# 4. Protected routes WITH token → 200:
curl -X POST http://localhost:8000/diagnostics \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"hostname":"Localhost","service":"sshd"}'

curl http://localhost:8000/audit-history \
  -H "Authorization: Bearer $TOKEN"

# 5. Garbage token → 401:
curl http://localhost:8000/audit-history \
  -H "Authorization: Bearer garbage"
```

### Swagger UI (interactive)

1. Open `http://localhost:8000/docs` (or `https://diagnostics.local/docs`
   via the ingress).
2. Click **Authorize** (padlock button, top right).
3. Enter `API_USERNAME` / `API_PASSWORD` — Swagger calls `/token` for you
   and attaches `Authorization: Bearer <jwt>` to every "Try it out" request.
4. After 30 minutes, re-Authorize to get a fresh token.

---

## 6. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `401 Invalid or expired token` | Token older than 30 min, or `JWT_SECRET_KEY` was rotated | Request a fresh token from `/token` |
| `401 Incorrect username or password` at `/token` | Credentials don't match Infisical values in the K8s Secret | Check Infisical values; rerun CD to sync the secret |
| Pods stuck in `CreateContainerConfigError` | `diagnostics-secret` missing `API_USERNAME` / `API_PASSWORD` / `JWT_SECRET_KEY` | Add keys in Infisical, rerun CD |
| Spurious expiry errors after Mac sleep | Docker Desktop VM clock drift | Restart Docker Desktop (or add `leeway=30` to `jwt.decode`) |
| `/token` returns 422 | Sent JSON instead of form data | Use `-d 'username=..&password=..'` (form-encoded) |
| CD workflow stuck in "Queued" | Self-hosted runner not running on the Mac | `cd ~/github-runner/diagnostics-api-project/actions-runner && ./run.sh` |
