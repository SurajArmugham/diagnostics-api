Incident Diagnostics API - Project History & Learning Context

Project Goal

Build an SRE-focused Incident Diagnostics API demonstrating:

* FastAPI
* PostgreSQL
* Paramiko SSH
* Docker
* Docker Compose
* GitHub Actions CI/CD
* Kubernetes

The project is intended for:

* SRE interviews
* DevOps interviews
* Platform Engineering interviews
* Hands-on infrastructure learning

⸻

Phase 1 - FastAPI Application

Built REST API endpoints for:

* Health checks
* Incident diagnostics
* SSH execution
* Audit logging

Technology:

* FastAPI
* Python

⸻

Phase 2 - SSH Diagnostics

Implemented SSH connectivity using Paramiko.

Diagnostic Target:

Mac Host

Examples:

* Disk usage
* Memory usage
* Open files
* Network commands

Architecture:

User
↓
FastAPI
↓
SSH
↓
Target Host

⸻

Phase 3 - PostgreSQL Integration

Implemented:

* Audit table creation
* Audit inserts
* Diagnostic execution history

Database:

PostgreSQL 16

⸻

Phase 4 - Dockerization

Created:

Dockerfile

Containerized:

* FastAPI Application

Learned:

* Docker Build
* Docker Run
* Image Layers
* Container Networking

⸻

Phase 5 - Docker Compose

Created:

docker-compose.yml

Services:

* diagnostics-api
* postgres-db

Learned:

* Multi-container deployment
* Environment variables
* Volumes
* Service discovery

Architecture:

diagnostics-api
↓
postgres-db

⸻

Phase 6 - GitHub Actions CI/CD

GitHub Repository:

diagnostic_api

Deployment Target:

Mac Self Hosted Runner

Diagnostic Target:

Mac SSH Service

Pipeline:

CI:

* Checkout
* Python Setup
* Install Dependencies
* Pytest

Current Scope:

Testing and validation only.

Future Enhancement:

* Docker Build
* Docker Hub Push

CD (Manual Workflow):

* Docker Compose Deployment
* Health Check

Key Learning:

Deployment target and diagnostic target are independent concepts.

Deployment Target:
Mac Docker Host

Diagnostic Target:
SSH-accessible Mac

⸻

Phase 6 Architecture

GitHub
↓
GitHub Actions
↓
Self Hosted Runner
↓
Docker Compose
↓
Diagnostics API

⸻

Phase 7 - Kubernetes CD

GitHub Repository:

diagnostic_api

Deployment Target:

Docker Desktop Kubernetes

Deployment Method:

GitHub Actions Manual Workflow

Workflow:

k8s-cd.yml

Deployment Flow:

GitHub Action
↓
Self Hosted Runner
↓
kubectl
↓
kubeconfig (~/.kube/config)
↓
Kubernetes API Server
↓
Control Plane
↓
Pods

Deployment Validation:

* kubectl apply -f k8s/
* sleep 10
* kubectl get pods
* kubectl port-forward service/diagnostics-api 8000:8000
* curl http://localhost:8000/health

Smoke Test Result:

{"status":"UP"}

Key Learning:

The GitHub runner does not require Kubernetes to run locally inside the workflow.

The runner only requires:

* kubectl
* kubeconfig
* Network access to Kubernetes API Server

Kubernetes CD Status:

✓ Working Successfully

⸻

Phase 7 - Kubernetes

Cluster:

Docker Desktop Kubernetes

Context:

docker-desktop

Node:

desktop-control-plane

Verified:

kubectl cluster-info
kubectl get nodes

⸻

Kubernetes Objects Implemented

Deployment

diagnostics-api

Purpose:

* Pod lifecycle
* Replica management
* Rolling updates

ReplicaSet

Automatically created by Deployment.

Observed:

Deployment
↓
ReplicaSet
↓
Pods

Pods

Diagnostics API Pods

Scaling Demonstrated:

replicas: 1 → 3

Services

Created:

diagnostics-api
postgres-db

Type:

ClusterIP

Learned:

Service Discovery
Label Selectors
Endpoints

Example:

postgres-db
↓
10.96.x.x

ConfigMap

Created:

diagnostics-config

Contains:

DB_HOST
DB_PORT
DB_NAME
SSH_HOST
SSH_PORT

Purpose:

Non-sensitive configuration.

Secret

Created:

diagnostics-secret

Contains:

DB_USER
DB_PASSWORD
SSH_USER
SSH_PASSWORD

Purpose:

Sensitive configuration.

⸻

CrashLoopBackOff Troubleshooting

Observed:

Unable to connect to database.

Root Cause:

PostgreSQL not deployed inside Kubernetes.

Resolution:

Created:

postgres-deployment.yaml
postgres-service.yaml

Application became healthy.

⸻

Service Discovery

Application connects using:

DB_HOST=postgres-db

Not:

Pod IP

Reason:

Pods are ephemeral.

Services provide stable DNS names.

⸻

Port Forwarding

Learned:

kubectl port-forward service/diagnostics-api 8000:8000

Testing:

curl http://localhost:8000/health

Response:

{“status”:“UP”}

⸻

Scaling

Changed:

replicas: 1

to:

replicas: 3

Observed:

3 Pods
1 Service

Endpoints:

10.244.x.x
10.244.x.x
10.244.x.x

⸻

Readiness Probe

Endpoint:

/health

Purpose:

Controls traffic routing.

Question:

Can this Pod receive traffic?

⸻

Liveness Probe

Endpoint:

/health

Purpose:

Automatic recovery.

Question:

Should Kubernetes restart this container?

⸻

Persistent Volume Claim (PVC)

Created:

postgres-pvc

Purpose:

Persistent storage request for PostgreSQL.

Learned:

* PVC remains Pending until consumed by a Pod.
* StorageClass dynamically provisions storage.
* PVC binds to a PV.
* Data survives Pod recreation.

Observed:

PVC Created
↓
Pending
↓
PostgreSQL Pod Mounted PVC
↓
PV Automatically Created
↓
PVC Bound

⸻

Persistent Volume (PV)

Automatically Created:

pvc-4d0f0262-1af4-46db-a77b-2a8256b6bedb

Purpose:

Actual storage resource backing the PVC.

Learned:

* Dynamic provisioning through StorageClass.
* PV created automatically by Kubernetes.
* Bound to postgres-pvc.

⸻

Stateful Workload Verification

Test Performed:

* Created pvc_test table.
* Inserted test record.
* Deleted PostgreSQL Pod.
* Kubernetes recreated PostgreSQL Pod.
* Verified data still existed.

Result:

Persistent storage successfully retained database data after Pod recreation.

Architecture:

PostgreSQL Pod
↓
Volume Mount
↓
PersistentVolumeClaim
↓
PersistentVolume
↓
Host Storage

⸻

Storage Concepts Learned

✓ Persistent Volume (PV)
✓ Persistent Volume Claim (PVC)
✓ StorageClass
✓ Dynamic Provisioning
✓ WaitForFirstConsumer
✓ Stateful Workloads
✓ Data Persistence Across Pod Recreation

⸻

Resource Requests and Limits

Implemented:

* diagnostics-api Deployment
* postgres-db Deployment

Purpose:

Control CPU and Memory allocation for Kubernetes workloads.

Diagnostics API Configuration:

Requests:
* CPU: 100m
* Memory: 128Mi

Limits:
* CPU: 500m
* Memory: 512Mi

PostgreSQL Configuration:

Requests:
* CPU: 250m
* Memory: 256Mi

Limits:
* CPU: 1
* Memory: 1Gi

Learned:

* Requests determine scheduling decisions.
* Limits define maximum resource consumption.
* Kubernetes Scheduler uses requests when placing Pods.
* Limits protect nodes from resource exhaustion.

QoS Classes Learned:

BestEffort
-----------
No requests or limits defined.

Burstable
----------
Requests and limits defined.

Guaranteed
-----------
Requests equal limits.

Verification:

Observed in:

kubectl describe pod diagnostics-api-xxxx
kubectl describe pod postgres-db-xxxx

Result:

QoS Class changed from:

BestEffort
↓
Burstable

Interview Learning:

Requests -> Scheduling
Limits -> Resource Enforcement

⸻

⸻

Kubernetes Concepts Learned

✓ Cluster
✓ Node
✓ Deployment
✓ ReplicaSet
✓ Pod
✓ Service
✓ ConfigMap
✓ Secret
✓ Labels
✓ Selectors
✓ Service Discovery
✓ Port Forwarding
✓ Scaling
✓ Rolling Updates
✓ Readiness Probe
✓ Liveness Probe
✓ Persistent Volume
✓ Persistent Volume Claim
✓ StorageClass
✓ Dynamic Provisioning
✓ Stateful Workloads
✓ Data Persistence Testing
✓ Resource Requests
✓ Resource Limits
✓ QoS Classes
✓ Burstable QoS Verification
✓ kubectl exec
✓ kubectl logs
✓ kubectl describe
✓ Ingress Controller
✓ IngressClass
✓ Host-Based Routing
✓ Path-Based Routing
✓ TLS Secret
✓ HTTPS
✓ TLS Termination
✓ OpenSSL Certificate Management

⸻

Ingress Controller

Installed:

ingress-nginx

Namespace:

ingress-nginx

Verified:

kubectl get pods -n ingress-nginx
kubectl get svc -n ingress-nginx
kubectl get ingressclass

Learned:

* Ingress Controller acts as a Layer 7 reverse proxy.
* Similar to NGINX / Apache HTTPD reverse proxy concepts.
* Receives HTTP/HTTPS traffic and routes requests to Services.
* Ingress is not a replacement for Services.
* Ingress sits in front of Services.

Architecture:

Client
↓
Ingress Controller
↓
Service
↓
Pods

⸻

Host-Based Routing

Implemented:

Host:

diagnostics.local

Ingress Rule:

Host: diagnostics.local
↓
diagnostics-api Service

Learned:

* Host header determines routing decisions.
* Requests with unmatched Host headers return 404 from NGINX.
* Ingress evaluates Host rules before forwarding traffic.

Validation:

curl http://localhost:8080/health \
-H "Host: diagnostics.local"

Result:

{"status":"UP"}

⸻

Path-Based Routing

Implemented:

* /
* /health
* /docs

Backend:

All paths currently route to diagnostics-api Service.

Learned:

* A single hostname can route multiple paths.
* Enterprise environments often route different paths to different Services.
* Longest matching path is evaluated first.

Enterprise Example:

api.company.com/docs
↓
documentation-service

api.company.com/api
↓
backend-service

api.company.com/health
↓
health-service

⸻

TLS / HTTPS

Created:

certs/
├── diagnostics.local.crt
└── diagnostics.local.key

Generated Using:

OpenSSL

Command:

openssl req -x509 ...

Learned:

* Self-signed certificate creation.
* Certificate contains public key.
* Private key must remain protected.
* HTTPS requires certificate + private key.

Certificate Verification:

openssl x509 -in diagnostics.local.crt -text -noout

Observed:

Subject: CN=diagnostics.local
Issuer: CN=diagnostics.local

Result:

Self-signed certificate.

⸻

Kubernetes TLS Secret

Created:

diagnostics-tls

Type:

kubernetes.io/tls

Contains:

* tls.crt
* tls.key

Learned:

Opaque Secret
-------------
Application credentials.

TLS Secret
----------
Certificates and private keys.

Verification:

kubectl describe secret diagnostics-tls

Observed:

tls.crt
tls.key

⸻

TLS Termination

Implemented:

Browser
↓ HTTPS
Ingress Controller
↓ HTTP
Service
↓
Pods

Learned:

* Application does not need to implement HTTPS.
* Ingress can terminate TLS.
* Internal cluster traffic can remain HTTP.
* Most enterprise Kubernetes deployments use TLS termination.

Ingress Verification:

kubectl describe ingress diagnostics-api-ingress

Observed:

TLS:
  diagnostics-tls terminates diagnostics.local

⸻

HTTPS Validation

Port Forward:

kubectl port-forward service/ingress-nginx-controller \
-n ingress-nginx 8080:80 8443:443

HTTP Test:

curl http://localhost:8080/health \
-H "Host: diagnostics.local"

HTTPS Test:

curl -k https://localhost:8443/health \
-H "Host: diagnostics.local"

Result:

{"status":"UP"}

TLS Verification:

openssl s_client \
-connect localhost:8443 \
-servername diagnostics.local

Observed:

subject=CN=diagnostics.local
issuer=CN=diagnostics.local
Protocol: TLSv1.3

Learned:

* TLS handshake validation.
* Certificate inspection.
* HTTPS troubleshooting.
* Self-signed certificate behavior.

⸻

Ingress Concepts Learned

✓ Ingress Controller
✓ IngressClass
✓ Host-Based Routing
✓ Path-Based Routing
✓ Reverse Proxy Concepts
✓ TLS Certificates
✓ OpenSSL
✓ TLS Secret
✓ HTTPS
✓ TLS Termination
✓ TLS Validation
✓ Certificate Inspection



⸻

Phase 8 - Infisical Cloud Secret Management

Objective

Introduce centralized secret management into the Kubernetes deployment pipeline while keeping application code and Kubernetes deployment manifests unchanged.

The goal is to simulate a common enterprise secret-management workflow where application credentials are stored in a dedicated secret-management platform rather than in source control.

⸻

Previous Secret Management Model

secret.yaml
↓
Kubernetes Secret
↓
Pods

Limitations:

* Secret rotation required manifest updates.
* Credentials could exist in multiple locations.
* Git repositories could become a source of truth for secrets.
* Difficult to demonstrate centralized secret management.

⸻

Selected Solution

Evaluated:

* HashiCorp Vault OSS
* HashiCorp Cloud Vault
* Cloud Secret Managers
* Infisical Cloud

Selected:

Infisical Cloud

Reasons:

* Free tier available.
* Cloud-hosted solution.
* No infrastructure management required.
* Supports Machine Identities.
* Supports Universal Authentication.
* Supports API-based secret retrieval.
* Supports secret rotation demonstrations.
* Closely resembles enterprise secret-management workflows.

⸻

Infisical Configuration

Created:

Project:
diagnostic-api

Environment:
dev

Stored Secrets:

* DB_USER
* DB_PASSWORD
* SSH_USER
* SSH_PASSWORD

Created:

Machine Identity:
github-actions

Role:
Viewer

Permissions:

diagnostic-api / dev

Learned:

Principle Of Least Privilege

The deployment workflow only requires permission to read secrets.

⸻

Universal Authentication

Implemented:

GitHub Actions
↓
INFISICAL_CLIENT_ID
INFISICAL_CLIENT_SECRET
↓
Universal Auth
↓
Access Token
↓
Infisical APIs

Validation:

Successfully authenticated using:

POST
/api/v1/auth/universal-auth/login

Observed:

* accessToken
* expiresIn
* tokenType

Result:

Authentication Successful

⸻

Secret Retrieval Validation

Validated:

* List Secrets API
* Get Secret By Name API

Successfully Retrieved:

* DB_USER
* DB_PASSWORD
* SSH_USER
* SSH_PASSWORD

Architecture:

GitHub Actions
↓
Universal Auth
↓
Access Token
↓
Infisical Cloud
↓
Application Secrets

Result:

Authorization Successful

⸻

GitHub Actions Integration

Enhanced:

.github/workflows/k8s-cd.yml

Added:

* Infisical Authentication
* Access Token Generation
* Secret Retrieval
* jq JSON Parsing
* Dynamic Kubernetes Secret Creation

Deployment Flow:

GitHub Actions
↓
Self Hosted Runner
↓
Infisical Cloud
↓
Secret Retrieval
↓
diagnostics-secret
↓
kubectl apply -f k8s/
↓
Pods

⸻

Dynamic Kubernetes Secret Creation

Implemented:

kubectl create secret generic diagnostics-secret

Type:

Opaque

Contains:

* DB_USER
* DB_PASSWORD
* SSH_USER
* SSH_PASSWORD

Result:

Application consumed dynamically generated secrets without requiring code changes.

⸻

Secret Recreation Validation

Test Performed:

kubectl delete secret diagnostics-secret

Observed:

Secret removed from cluster.

Action:

Executed Kubernetes CD workflow.

Observed:

GitHub Actions
↓
Infisical Authentication
↓
Secret Retrieval
↓
Kubernetes Secret Recreation

Verification:

kubectl describe secret diagnostics-secret

Observed:

Type: Opaque

DB_USER
DB_PASSWORD
SSH_USER
SSH_PASSWORD

Result:

Secret recreated successfully from Infisical.

⸻

Secret Rotation Capability

Current Capability:

Infisical
↓
Update Secret
↓
Run Kubernetes CD Workflow
↓
Retrieve Latest Secret
↓
Update Kubernetes Secret
↓
Pods Consume Updated Secret

Benefits:

* No application code changes.
* No Git commits required.
* No Kubernetes manifest updates required.
* Centralized source of truth.
* Enterprise-style secret lifecycle management.

⸻

Additional Concepts Learned

✓ Centralized Secret Management
✓ Machine Identity
✓ Universal Authentication
✓ Access Tokens
✓ Bearer Authentication
✓ Secret Retrieval APIs
✓ Authorization vs Authentication
✓ Principle Of Least Privilege
✓ Dynamic Kubernetes Secret Creation
✓ Secret Lifecycle Automation
✓ Secret Rotation Concepts
✓ jq JSON Parsing
✓ Infisical Cloud Integration

⸻

Phase 9 - JWT Bearer Authentication

Objective

Secure all business endpoints of the API. Previously every endpoint was anonymous - anyone reaching the API could trigger SSH sessions into the host or read the audit trail.

The goal is to implement the same machine-to-machine authentication pattern already used by the CD pipeline against Infisical (credentials → access token → Bearer header), but with our API acting as the token issuer and verifier instead of consuming someone else's.

⸻

Authentication Model

Client
↓
POST /token
(API_USERNAME + API_PASSWORD, form-encoded)
↓
Signed JWT
(HS256, JWT_SECRET_KEY, 30 minute expiry)
↓
Authorization: Bearer <jwt>
↓
Protected Routes

Protected:

* POST /diagnostics
* GET /audit-history

Open (Kubernetes probes require it):

* GET /health

⸻

Key Decisions

* PyJWT for token signing and verification.
* OAuth2PasswordBearer scheme - enables the Swagger UI Authorize button at /docs.
* /token accepts OAuth2 password form data (requires python-multipart).
* Router-level dependency - APIRouter(dependencies=[Depends(verify_token)]) protects all diagnostics routes in one line.
* Constant-time credential comparison (secrets.compare_digest, both fields, no short-circuit) to prevent timing attacks.
* Expiry lives INSIDE the token as the exp claim - no server-side timer, verified per request by jwt.decode().
* Stateless verification - all 3 replicas share JWT_SECRET_KEY, any pod validates any token.

⸻

Secret Management Integration

Infisical Cloud gained three new secrets:

* API_USERNAME
* API_PASSWORD
* JWT_SECRET_KEY

Flow unchanged:

Infisical Cloud
↓
Kubernetes CD Workflow
↓
diagnostics-secret
↓
Pod Environment Variables

Rotating JWT_SECRET_KEY in Infisical and rerunning CD instantly invalidates all outstanding tokens - the standard "log everyone out" lever.

⸻

Testing Strategy

tests/conftest.py injects dummy credentials (testuser / testpass / test-secret-key) into os.environ before the app loads.

Consequences:

* pytest is fully self-contained on the GitHub-hosted runner.
* No new GitHub secrets required for CI.
* Real credentials never touch the test suite.

New tests (11 total passing):

* Token issuance success
* Wrong password → 401
* Missing token → 401
* Garbage token → 401
* Hand-crafted expired token → 401
* /health open without token → 200

⸻

CI/CD Enhancements

CI (ci.yml):

* Docker build / login / tag / push steps enabled.
* Build runs on pushes AND pull requests (Dockerfile validation).
* Login / Tag / Push gated:
  if: github.event_name == 'push' && github.ref == 'refs/heads/main'
* Pull requests validate but never publish artifacts.

CD (k8s-cd.yml) - GitOps single-apply design:

* No runtime image mutation (no kubectl set image, no image_tag input).
* The tag pinned in k8s/deployment.yaml is the single source of truth - each release is exactly one rollout and the cluster always mirrors Git.
* Release flow: push code → CI pushes image :<git-sha> → verify on Docker Hub → pin <git-sha> in manifests → commit "[skip ci]" → push → run Kubernetes CD.
* kubectl rollout status replaces fixed sleep (fails fast on image pull errors / crash loops).
* Infisical step retrieves the 3 new auth secrets (7 total).
* Smoke test extended: unauthenticated POST /diagnostics must return 401 - proves authentication is live without credentials on the runner.

Lesson Learned (the hard way):

GitHub skips push-triggered workflows when the head commit message contains "[skip ci]" ANYWHERE - including in descriptive prose. A commit message that merely documented the flow ("... commit [skip ci] -> run CD") silently suppressed the CI run. Diagnosis path: push event registered, workflows active, Actions operational, no run created → inspect the commit message. Fix: empty retrigger commit.

⸻

Documentation

auth_guide.md created:

* Token request commands and expiry inspection.
* Secret update checklist (Infisical / GitHub / local).
* Cluster + self-hosted runner bring-up steps.
* Post-deployment verification flow.
* Troubleshooting table.

⸻

Additional Concepts Learned

✓ JWT Structure (header.payload.signature)
✓ Opaque Tokens vs Self-Contained Tokens
✓ OAuth2 Password Flow
✓ Bearer Token Scheme (RFC 6750)
✓ Token Expiry (exp claim)
✓ Stateless Authentication
✓ Constant-Time Comparison / Timing Attacks
✓ Router-Level Dependencies (FastAPI)
✓ Swagger UI Authorize Integration
✓ CI Publish Gating (push vs pull_request)
✓ kubectl set image / Rollout Status
✓ Secret Rotation As Token Revocation

⸻

Phase 10 - Monitoring & Observability

Roadmap:

10.1 Structured JSON logging to stdout       ✓ SHIPPED
10.2 /metrics endpoint (Prometheus client)   ✓ SHIPPED
10.3 Prometheus deployment in-cluster
10.4 Grafana dashboards + alerting
10.5 Log aggregation (Loki hands-on + Splunk enterprise notes)

⸻

Phase 10.1 - Structured JSON Logging to stdout

Objective

Make application logs COLLECTABLE (stdout) and QUERYABLE (JSON). Previously the app wrote plain-text logs to logs/app.log inside the container - invisible to kubectl logs, invisible to any log collector, and lost on every pod restart.

⸻

The Kubernetes Log Pipeline

app stdout
↓
container runtime
↓
/var/log/containers/*.log   (on the node)
↓
collector DaemonSet (Alloy / Splunk forwarder / promtail)
↓
Loki / Splunk

A file inside the pod sits OFF this conveyor belt. Writing to stdout is the contract with the platform (12-Factor App, factor XI: an app never routes or stores its own log stream).

⸻

Implementation

app/utils/logger.py rewritten:

* JsonFormatter - stdlib-only logging.Formatter subclass (~20 lines: override format(), return json.dumps). This is what python-json-logger does under the hood.
* Each line: timestamp (UTC ISO-8601), level, logger, message.
* extra={...} fields at the call site are promoted to top-level JSON keys.
* exc_info tracebacks captured under an "exception" key.
* NAMED logger ("diagnostics_api") with propagate=False - NOT basicConfig, which configures the ROOT logger and captures every library's propagated records into your format.
* Call sites unchanged (5 modules import the same logger object).

tests/test_logger.py: valid-JSON, extra-fields, exception-capture (suite: 14 tests).

⸻

Why JSON At The Source

Plain:  2026-07-16 10:32:01 WARNING Failed login attempt
JSON:   {"level": "WARNING", "message": "Failed login attempt", ...}

Plain text forces Splunk/Loki to regex-guess fields out of prose - brittle, breaks when wording changes. JSON makes every key an instantly searchable field:

level=WARNING | stats count by client_ip

⸻

Release Process Lessons

* Released via the canonical GitOps runbook: push → CI image → verify Docker Hub → pin sha in manifests → [skip ci] push → manual CD.
* ROLLING UPDATE, not restart: the release deployed to the LIVE cluster. New pods passed readiness probes before old pods terminated (pod AGE stagger: 2m42s / 2m14s / 2m02s). Never stop a cluster to deploy - that is the pre-Kubernetes mental model.
* Runner preflight must be PATH-SPECIFIC: a generic pgrep for Runner.Listener false-positived on a second runner install (incident-project). Check the full install path.

⸻

Verification (payoff)

kubectl logs -l app=diagnostics-api now shows the app's own events:

{"timestamp": "2026-07-16T16:53:15.526399+00:00", "level": "WARNING", "logger": "diagnostics_api", "message": "Failed login attempt"}

Observed along the way:

* Kubelet probe traffic (INFO "Health endpoint called" every 5s per pod) - previously invisible.
* kubectl logs -l defaults to --tail=10 per pod - grepping tails does not scale; THIS is the problem log aggregation (10.5) solves.

⸻

Additional Concepts Learned

✓ Three Pillars (Metrics / Logs / Traces)
✓ 12-Factor Logging (Factor XI)
✓ Kubernetes Log Pipeline (stdout → node files → DaemonSet collector)
✓ Structured Logging / Fields vs Regex Extraction
✓ Named Logger vs Root basicConfig
✓ Logger Propagation
✓ Rolling Updates vs Restart-To-Deploy
✓ Path-Specific Process Checks

⸻

Phase 10.2 - Prometheus /metrics Endpoint

Objective

Expose application metrics in Prometheus format so the metrics pillar becomes real: automatic request metrics for every endpoint, plus custom security counters that turn Phase 9's auth events into graphable numbers.

⸻

Implementation

* prometheus-fastapi-instrumentator wired in run.py:
  instrument(app) - middleware records RED metrics per request
  (Rate, Errors, Duration):
  http_requests_total{handler, method, status}
  http_request_duration_seconds (histogram)
  expose(app) - mounts GET /metrics (Prometheus text format).

* Custom counters in app/utils/metrics.py:
  tokens_issued_total
  auth_failures_total{reason="bad_credentials" | "invalid_token"}
  Incremented in routes/auth.py (login) and auth/dependencies.py (verify).

* tests/test_metrics.py - endpoint open, RED metrics recorded,
  every counter increments exactly once (suite: 19 tests).

⸻

Design Decisions

* /metrics is OPEN (like /health): the industry standard. Prometheus
  PULLS from inside the cluster; production restricts access by
  NETWORK (NetworkPolicy / internal-only), not application auth.
  Lab note: reachable via diagnostics.local/metrics through the
  ingress catch-all - acceptable for learning, listed as a
  production-hardening item.

* Pull vs Push: the app stays passive - no metrics pipeline in app
  code. A dead app is DETECTED because the scrape fails (up == 0),
  which is itself an alertable signal.

* Counter semantics: counters only increase (reset on pod restart).
  PromQL rate() converts them to per-second rates:
  rate(auth_failures_total[5m])

* Label cardinality: every distinct label value creates a new time
  series. Labels must be small bounded sets (reason has 2 values).
  Never usernames, IPs, or request IDs.

⸻

Verified In Production (and a live lesson)

curl -sk https://diagnostics.local/metrics after generating traffic:

tokens_issued_total 0.0
auth_failures_total{reason="invalid_token"} 1.0
http_requests_total{handler="/health",...} 45.0    ← kubelet probes, now measurable

The test traffic was load-balanced across 3 replicas - the scraped pod
showed invalid_token=1 but NOT the bad_credentials hit (it landed on a
sibling pod). Each replica counts only its own traffic: THIS is why
Prometheus scrapes every pod individually and aggregates with

sum(rate(auth_failures_total[5m]))

⸻

Additional Concepts Learned

✓ RED Method (Rate, Errors, Duration)
✓ Pull vs Push Metrics Models
✓ Prometheus Text Exposition Format
✓ Counter vs Gauge vs Histogram
✓ Label Cardinality Discipline
✓ Per-Replica Counters → PromQL sum()
✓ Open Metrics Endpoint + Network Restriction Pattern



Current Architecture

GitHub Actions
↓
Self Hosted Runner
↓
Infisical Cloud
↓
Universal Auth
↓
Access Token
↓
Kubernetes Secret (diagnostics-secret)
↓
kubectl
↓
Docker Desktop Kubernetes
↓
Ingress Controller
↓
Service (diagnostics-api)
↓
3 FastAPI Pods
↓
Service (postgres-db)
↓
PostgreSQL Pod

Configuration:

ConfigMap
↓
Non-Sensitive Configuration

Infisical Cloud
↓
Kubernetes Secret
↓
Sensitive Configuration
(DB, SSH, API auth credentials, JWT signing key)

Authentication:

Client
↓
POST /token
↓
Bearer JWT (30 min)
↓
Protected Routes
(/diagnostics, /audit-history)

/health remains open for probes.

Health:

Readiness Probe
Liveness Probe

⸻

Phase Status

✓ Phase 1 - FastAPI
✓ Phase 2 - SSH Diagnostics
✓ Phase 3 - PostgreSQL
✓ Phase 4 - Docker
✓ Phase 5 - Docker Compose
✓ Phase 6 - GitHub Actions CI/CD
✓ Phase 7 - Kubernetes
✓ Phase 7 - Kubernetes CD
✓ Phase 8 - Infisical Secret Management
✓ Phase 9 - JWT Bearer Authentication
✓ Phase 10.1 - Structured JSON Logging
✓ Phase 10.2 - Prometheus /metrics Endpoint
