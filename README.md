Incident Diagnostics API

A hands-on Site Reliability Engineering (SRE) and Platform Engineering learning project built with FastAPI, PostgreSQL, Docker, GitHub Actions, and Kubernetes.

The project simulates a diagnostics platform capable of executing system-level checks over SSH, storing audit history in PostgreSQL, and running in both Docker Compose and Kubernetes environments.

⸻

Project Goals

This project was built to gain practical experience with:

* Python API development
* Linux diagnostics
* SSH automation
* PostgreSQL integration
* Docker and Docker Compose
* GitHub Actions CI/CD
* Kubernetes deployments
* Kubernetes networking
* Kubernetes storage
* Ingress and TLS
* Centralized Secret Management (Infisical)

The project is designed as a portfolio project for:

* SRE Interviews
* DevOps Interviews
* Platform Engineering Interviews
* Infrastructure Engineering Interviews

⸻

Features

API Health Checks

Validate application availability.

Endpoint:

GET /health

Response:

{
  "status": "UP"
}

⸻

SSH Diagnostics

Execute remote diagnostic commands through SSH.

Examples:

* Disk Usage
* Memory Usage
* Open Files
* Network Diagnostics

Architecture:

User
 ↓
FastAPI
 ↓
SSH (Paramiko)
 ↓
Target Host

⸻

Audit Logging

Stores diagnostic execution history in PostgreSQL.

Examples:

* Command Executed
* Execution Timestamp
* Diagnostic Results

⸻

Technology Stack

Component	Technology
API	FastAPI
Language	Python
Database	PostgreSQL 16
SSH Library	Paramiko
Containerization	Docker
Local Orchestration	Docker Compose
CI/CD	GitHub Actions
Kubernetes	Docker Desktop Kubernetes
Ingress	ingress-nginx
TLS	OpenSSL
Storage	PVC / PV
Secret Management	Infisical Cloud

⸻

Architecture

Kubernetes Deployment

GitHub Actions
        ↓
Self Hosted Runner
        ↓
Infisical Cloud
        ↓
Universal Auth
        ↓
Kubernetes Secret
        ↓
kubectl
        ↓
kubeconfig
        ↓
Kubernetes API Server
        ↓
Control Plane
        ↓
Ingress Controller (HTTPS)
        ↓
diagnostics-api Service
        ↓
3 FastAPI Pods
        ↓
postgres-db Service
        ↓
PostgreSQL Pod
        ↓
Persistent Volume Claim
        ↓
Persistent Volume

⸻

Kubernetes Features Implemented

Workload Management

* Deployments
* ReplicaSets
* Pods
* Scaling

Current Deployment:

diagnostics-api
Replicas: 3

⸻

Networking

Services

Implemented:

* diagnostics-api
* postgres-db

Service Type:

ClusterIP

Ingress

Implemented:

* Host-Based Routing
* Path-Based Routing
* TLS Termination

Examples:

https://diagnostics.local/health
https://diagnostics.local/docs

⸻

Configuration Management

ConfigMap

Used for:

DB_HOST
DB_PORT
DB_NAME
SSH_HOST
SSH_PORT

Secret

Source:

Infisical Cloud
        ↓
GitHub Actions
        ↓
diagnostics-secret

Used for:

DB_USER
DB_PASSWORD
SSH_USER
SSH_PASSWORD

Learned:

* Machine Identities
* Universal Authentication
* Access Tokens
* Secret Retrieval APIs
* Secret Rotation Concepts

TLS Secret

Used for:

tls.crt
tls.key

⸻

Storage

Implemented:

* Persistent Volume Claims (PVC)
* Persistent Volumes (PV)
* Dynamic Provisioning

Validation Performed:

Create Table
     ↓
Insert Data
     ↓
Delete PostgreSQL Pod
     ↓
Pod Recreated
     ↓
Data Still Exists

Result:

Persistent storage verified successfully.

⸻

Health Checks

Readiness Probe

Purpose:

Can this Pod receive traffic?

Endpoint:

/health

Liveness Probe

Purpose:

Should Kubernetes restart this Pod?

Endpoint:

/health

⸻

Resource Management

Diagnostics API:

Requests
CPU: 100m
Memory: 128Mi
Limits
CPU: 500m
Memory: 512Mi

PostgreSQL:

Requests
CPU: 250m
Memory: 256Mi
Limits
CPU: 1
Memory: 1Gi

⸻

CI/CD

Continuous Integration

GitHub Actions CI Pipeline:

Checkout
    ↓
Python Setup
    ↓
Install Dependencies
    ↓
Pytest

Current Scope:

* Build Validation
* Unit Testing

⸻

Continuous Deployment

Docker Compose Deployment

Manual GitHub Actions Workflow.

Deployment Target:

Mac Self Hosted Runner

Kubernetes Deployment

Manual GitHub Actions Workflow.

Deployment Flow:

GitHub Action
    ↓
Self Hosted Runner
    ↓
Infisical Cloud
    ↓
Secret Retrieval
    ↓
Kubernetes Secret
    ↓
kubectl

Validation:

kubectl apply -f k8s/
kubectl get pods
curl http://localhost:8000/health

⸻

Project Structure

diagnostic_api/
│
├── app/
├── tests/
│
├── certs/
│
├── k8s/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── postgres-deployment.yaml
│   ├── postgres-service.yaml
│   ├── postgres-pvc.yaml
│   ├── configmap.yaml
│   ├── secret-template.yaml
│   └── tls-secret.yaml
│
├── .github/
│   └── workflows/
│       ├── ci.yml
│       ├── cd.yml
│       └── k8s-cd.yml
│
├── Dockerfile
├── docker-compose.yml
├── docker-compose.deploy.yml
│
└── README.md

⸻

Learning Outcomes

Implemented and validated:

* FastAPI
* PostgreSQL
* Paramiko SSH
* Docker
* Docker Compose
* GitHub Actions
* Kubernetes Deployments
* ReplicaSets
* Pods
* Services
* ConfigMaps
* Secrets
* PVCs
* PVs
* StorageClasses
* Readiness Probes
* Liveness Probes
* Resource Requests
* Resource Limits
* Ingress Controllers
* Host-Based Routing
* Path-Based Routing
* TLS Certificates
* TLS Secrets
* HTTPS
* TLS Termination
* Machine Identity Authentication
* Universal Authentication
* Infisical Cloud
* Centralized Secret Management
* Secret Rotation Concepts
* Dynamic Kubernetes Secret Creation

⸻

Future Enhancements

Planned:

* Rolling Updates
* Rollbacks
* Horizontal Pod Autoscaler (HPA)
* Monitoring
* Alerting
* Advanced Troubleshooting Scenarios
* Prometheus
* Grafana
* cert-manager
* External Secrets Operator
* Secret Rotation Automation
* HashiCorp Vault Integration

⸻

Secret Management Architecture

Infisical Cloud
        ↓
Machine Identity
        ↓
Universal Authentication
        ↓
Access Token
        ↓
GitHub Actions
        ↓
Kubernetes Secret (diagnostics-secret)
        ↓
FastAPI Pods

Benefits:

* Centralized Secret Management
* No Credentials Stored In Git
* Secret Rotation Support
* Enterprise-style Secret Lifecycle Management
* Dynamic Kubernetes Secret Creation

suraj_armugham@ProBook diagnostic_api % curl -k https://localhost:8443/health \                
  -H "Host: diagnostics.local"
{"status":"UP"}                                             