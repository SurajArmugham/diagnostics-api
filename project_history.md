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
* Docker Build
* Docker Push

CD:

* Pull Latest Image
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

⸻

Current Architecture

User
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
Secret

Health:

Readiness Probe
Liveness Probe

Structure:
diagnostic_api/
│
├── app/
├── tests/
├── k8s/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── postgres-deployment.yaml
│   ├── postgres-service.yaml
│   ├── configmap.yaml
│   └── secret.yaml
│
├── Dockerfile
├── docker-compose.yml
├── docker-compose.deploy.yml
│
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── cd.yml
│
└── project_history.md

⸻

Next Planned Topics

1. Kubernetes CI/CD Deployment
2. Ingress
3. Advanced Troubleshooting
4. Monitoring
5. Alerting

⸻

Interview Readiness Topics Covered

Docker
Docker Compose
GitHub Actions
Self Hosted Runners
FastAPI
PostgreSQL
SSH
Kubernetes Deployments
Services
ConfigMaps
Secrets
Scaling
Rolling Updates
Readiness Probes
Liveness Probes