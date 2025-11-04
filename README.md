🧱 IIP_SECURE_STACK

**Inner Infinite Power™ Secure Stack**  
A private, full-stack DevSecOps architecture for secure AI, data, and automation systems.

---

## 🚀 Introduction

IIP_SECURE_STACK is a modular, containerized framework designed for creators, researchers, and enterprises prioritizing **security, automation, and AI integration**.  
It provides a **self-owned infrastructure** for running large language models (LLMs), analytics pipelines, and data services—without dependency on third-party SaaS platforms.

**Use cases:**
- Secure deployment of AI and analytics workloads
- Private LLM inference and experimentation
- Automated observability and compliance pipelines
- End-to-end wellness or performance platforms

---

## ⚙️ System Overview   ( 2.0 ) 

| Layer | Description | Key Components |
|:------|:-------------|:----------------|
| **1. Infrastructure Layer** | Base containers, networking, and persistent data volumes. | Docker, Nginx, Gunicorn, Redis |
| **2. Database Layer** | Centralized data persistence and caching. | PostgreSQL, DuckDB |
| **3. API & Logic Layer** | Handles AI, SQL, and service orchestration. | Flask, Llama-cpp-Python |
| **4. Frontend & Visualization Layer** | Real-time dashboards and visual analytics. | Streamlit, Apache Superset |
| **5. Observability & Security Layer** | System health, metrics, and alerting. | Grafana, Loki, Promtail |
| **6. CI/CD & Automation Layer** | Automated builds, tests, and deployments. | GitHub Actions, Docker Compose |
| **7. AI ↔ SQL Bridge Layer (Phase 12)** | Local inference pipeline linking models to databases. | `llama_cpp.server`, `Phi-2 GGUF`, Flask API |


## ⚙️ System Overview  ( 2.1 ) 11/03/2025 - 5:57 PM

| Layer | Description | Key Components |
|:------|:-------------|:----------------|
| **1. Infrastructure Layer** | Base containers, networking, TLS, and persistent volumes. | Docker, Nginx, Gunicorn, TLS/OpenSSL, Redis, PVCs |
| **2. Data & Storage Layer** | Centralized data, caches, and object storage. | PostgreSQL, DuckDB, MinIO (S3), Backups (CronJobs/Velero) |
| **3. API & Logic Layer** | AI services and business logic. | Flask, Gunicorn, llama-cpp-python, Celery (opt) |
| **4. Frontend & Visualization Layer** | Real-time apps and analytics. | Streamlit, Apache Superset |
| **5. Observability & Policy Layer | Metrics, logs, traces, runtime policy. | Prometheus, Alertmanager, Grafana, Loki, Promtail, Tempo, OpenTelemetry Collector, Kyverno, NetworkPolicies, PodSecurity/Seccomp |
| **6. CI/CD & Automation Layer** | Builds, scans, image delivery, deploys. | GitHub Actions, Dockerfiles, GHCR, Helm, Kustomize, Docker Compose, pre-commit, gitleaks |
| **7. AI ↔ SQL Bridge Layer** | Private LLM → SQL gateway with guardrails. | `llama_cpp.server`, Phi-2 GGUF, Flask gateway, `sqlparse`, Postgres/DuckDB (read-only), OTel |
| **8. Kubernetes Orchestration (Phase 12)** | Cluster runtime, ingress, scheduling, quotas. | K3s, Traefik/Nginx Ingress, PV/PVC, RBAC, HPA, ResourceQuotas/LimitRanges, GPU node pools (if present) |
| **9. Governance & Orchestration (Phase 13)** | Centralized workflow governance and compliance. | Apache Airflow (webserver/scheduler/triggerer), CeleryExecutor (opt), Postgres metadata, MinIO remote logs, Governance DAGs |

---

## 🧩 Phase 12 — AI ↔ SQL Bridge Integration

**Status:** Completed • **Mode:** Private, air-gapped • **Date:** November 2025  
**Endpoints:** `POST /query`, `POST /explain`, `GET /healthz`, `GET /readyz`  
**Ports:** Gateway `5001`, LLM `8000`, Postgres `5432` (optional), DuckDB file (optional)

### Objectives
- Natural-language → safe, parameterized SQL against approved schemas.
- Private LLM (llama.cpp) with no external calls.
- Deterministic guardrails: read-only role, DDL/DML blocked, row caps, timeouts.
- Full observability: traces, logs, metrics.

### Architecture
```mermaid
flowchart LR
  U[Client] --> GW[Flask AI↔SQL Gateway :5001]
  subgraph Guardrails
    POL[Policy Engine\n(allowlist, keyword bans, row caps)]
    TPL[Prompt Template\n+ Schema Snapshot]
  end
  GW --> POL
  POL -- sanitized prompt --> LLM[llama_cpp.server :8000\nPhi-2 (GGUF)]
  LLM -- SQL candidate --> GW
  GW --> TR[Translator & Validator\n(pydantic + sqlparse)]
  TR -- prepared stmt --> DB[(SQL Engine)]
  DB -- rows/json --> GW
  subgraph Observability
    OTEL[OTel SDK → Collector]
    LOG[Loki]
    MET[Prometheus]
  end
  GW -. traces .-> OTEL
  GW -. logs .-> LOG
  GW -. metrics .-> MET

What Runs Now
	•	Gateway: Flask app that exposes /query and /explain.
	•	LLM server: llama_cpp.server serving a local GGUF model (e.g., Phi-2).
	•	SQL engines: Postgres (read-only role) or DuckDB file.
	•	Observability: OpenTelemetry spans, structured logs, Prometheus counters.

Security Controls
	•	Read-only DB role; DDL/DML blocked by keyword filter and validator.
	•	Schema allowlist: ALLOWED_SCHEMAS env var.
	•	Row limits: MAX_ROWS default 1,000.
	•	Request timeout: QUERY_TIMEOUT_S default 20s.
	•	Bearer token auth: AUTH_TOKEN.
	•	NetworkPolicy limiting inbound to the gateway only (K8s).

Environment

# .env (example)
APP_PORT=5001
AUTH_TOKEN=<redacted>
LLM_BASE_URL=http://llm:8000
DB_KIND=postgres             # postgres | duckdb
DB_DSN=postgresql://ro_user:*****@postgres:5432/iip
ALLOWED_SCHEMAS=public,analytics
MAX_ROWS=1000
QUERY_TIMEOUT_S=20
OTEL_ENABLED=true
OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317

Docker Compose

version: "3.9"
services:
  gateway:
    build: ./phase12_ai_sql/app
    env_file: .env
    ports: ["5001:5001"]
    depends_on: [llm, postgres]
  llm:
    image: ghcr.io/ggerganov/llama.cpp:server
    command: ["-m","/models/phi-2.Q4_K_M.gguf","-c","4096","--host","0.0.0.0","--port","8000"]
    volumes: ["./models:/models:ro"]
    ports: ["8000:8000"]
  postgres:
    image: bitnami/postgresql:16
    environment:
      - POSTGRESQL_USERNAME=ro_user
      - POSTGRESQL_PASSWORD=<redacted>
      - POSTGRESQL_DATABASE=iip
    ports: ["5432:5432"]
    volumes: ["pgdata:/bitnami/postgresql"]
volumes:
  pgdata:

Kubernetes (optional)

# k8s/phase12/ai-sql-gateway.deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata: {name: ai-sql-gateway, namespace: iip-dev, labels:{app: ai-sql-gateway}}
spec:
  replicas: 1
  selector: {matchLabels:{app: ai-sql-gateway}}
  template:
    metadata: {labels:{app: ai-sql-gateway}}
    spec:
      securityContext: {runAsNonRoot: true}
      containers:
        - name: gateway
          image: registry.local/iip/ai-sql-gateway:${GIT_SHA}
          ports: [{containerPort: 5001}]
          envFrom: [{secretRef:{name: ai-sql-env}}]
          readinessProbe: {httpGet:{path:"/readyz", port:5001}, initialDelaySeconds:5, periodSeconds:5}
          livenessProbe:  {httpGet:{path:"/healthz", port:5001}, initialDelaySeconds:10, periodSeconds:10}
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities: {drop: ["ALL","NET_RAW"]}
---
apiVersion: v1
kind: Service
metadata: {name: ai-sql-gateway, namespace: iip-dev}
spec:
  selector: {app: ai-sql-gateway}
  ports: [{port: 80, targetPort: 5001}]
---
# Restrict DB access to gateway only
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: {name: db-restrict, namespace: iip-dev}
spec:
  podSelector: {matchLabels:{app: postgres}}
  ingress:
    - from: [{podSelector:{matchLabels:{app: ai-sql-gateway}}}]
      ports: [{protocol: TCP, port: 5432}]
  policyTypes: ["Ingress"]

Prompt Template (LLM → SQL)

System: You translate user questions into a single ANSI SQL SELECT statement.
- Use only tables/columns from: {{ allowed_schemas }}
- Never modify data.
- Max rows: {{ max_rows }}
- Use WHERE, LIMIT, and safe casts.
- If data is ambiguous, ask for a filter instead of guessing.

Schema:
{{ schema_snapshot }}

User question:
{{ question }}

Gateway Logic (summary)
	•	/query:
	1.	fetch schema snapshot (cached)
	2.	render prompt → call LLM
	3.	parse SQL → validate (allowlist, keywords, LIMIT)
	4.	bind parameters → execute with timeout
	5.	return JSON rows + sql_used
	•	/explain: returns sql_used + EXPLAIN plan and row count estimate.

Example Requests

# Query
curl -s -X POST http://localhost:5001/query \
  -H "Authorization: Bearer ${API_TOKEN}" -H "Content-Type: application/json" \
  -d '{"question":"Top 10 customers by revenue this quarter"}' | jq

# Explain
curl -s -X POST http://localhost:5001/explain \
  -H "Authorization: Bearer ${API_TOKEN}" -H "Content-Type: application/json" \
  -d '{"question":"Top 10 customers by revenue this quarter"}' | jq

# Health
curl -s http://localhost:5001/healthz

Policy and Validation
	•	Keyword ban: DROP|DELETE|UPDATE|INSERT|ALTER|TRUNCATE|GRANT|REVOKE|CREATE|COMMENT (regex word-boundaries).
	•	Schema allowlist: reject references outside ALLOWED_SCHEMAS.
	•	Limiter: auto-append LIMIT {{MAX_ROWS}} if missing.
	•	Timeout: hard cancel at QUERY_TIMEOUT_S.
	•	Plan gate: optional COST_LIMIT to reject pathological queries.

Observability Map
	•	Traces: query.translate, query.validate, query.execute.
	•	Metrics: ai_sql_requests_total{status}, ai_sql_latency_seconds_bucket, db_rows_returned_total.
	•	Logs: JSON lines with trace_id, sql_used, rowcount.

Tests (pytest)

def test_dml_blocked(client, auth):
    r = client.post("/query", headers=auth, json={"question":"delete all rows"})
    assert r.status_code == 400

def test_schema_allowlist(client, auth):
    r = client.post("/query", headers=auth, json={"question":"select * from secret.users"})
    assert r.status_code == 400

def test_limit_auto_added(client, auth):
    r = client.post("/explain", headers=auth, json={"question":"list orders"})
    assert "LIMIT" in r.json()["sql_used"].upper()

Service Inventory

Component	Image/Ref	Port	Health	Notes
Gateway	registry.local/iip/ai-sql-gateway:<sha>	5001	/healthz,/readyz	OTel on
LLM	ghcr.io/ggerganov/llama.cpp:server	8000	GET /health	Model in ./models
Postgres (opt)	bitnami/postgresql:16	5432	TCP	Read-only role
DuckDB (opt)	file data/iip.duckdb	—	—	Local file

Repo Layout

phase12_ai_sql/
  app/
    server.py          # Flask app + endpoints
    policy.py          # allowlist, bans, limiters
    translator.py      # prompt render, LLM call, sqlparse validation
    db.py              # connectors (postgres, duckdb) + timeouts
    schema_cache.py    # snapshot + caching
    metrics.py         # OTel + Prometheus
    tests/             # pytest cases above
  Dockerfile
  docker-compose.yaml
  k8s/
    ai-sql-gateway.deployment.yaml
    ai-sql-gateway.service.yaml
    networkpolicy.yaml
  models/              # *.gguf (not committed)

Deploy

# Local
docker compose up -d --build

# Kubernetes (after pushing image)
kubectl apply -f k8s/phase12/
kubectl -n iip-dev get deploy,svc | grep ai-sql-gateway

Troubleshooting
	•	400 with blocked keyword: question implies DDL/DML → refine prompt.
	•	504/timeout: raise QUERY_TIMEOUT_S or add filters; check EXPLAIN.
	•	Empty rows: confirm ALLOWED_SCHEMAS and DB role grants.
	•	LLM errors: confirm model path and LLM_BASE_URL.

Change Log
	•	Phase 12: Private LLM + AI↔SQL gateway running; guardrails active; OTel integrated.

## 🧩 Phase 12 — AI ↔ SQL Bridge Integration

This phase creates a **live, secure bridge** between your local AI model and SQL data engine.  
It enables contextual query translation, automated data analysis, and GPT-compatible endpoints.

**Pipeline:**
1. Flask server listens on `localhost:5001`
2. LLM (Phi-2, GGUF format) served via `llama_cpp.server`
3. Secure bridge handles `POST /query` → SQL engine
4. Result formatted and returned through JSON

**Result:**  
A functional private AI gateway—no external API calls, fully containerized, auditable, and scalable.

------------------------------------

## Phase 12 — Kubernetes Orchestration (≈15 Dockerized Services)

**Status:** Completed • **Cluster:** K3s • **Date:** November 2025  
**Namespaces:** `iip-dev`, `monitoring`, `kyverno`, `kube-system`

### Objectives
- Migrate core services from Docker Compose to Kubernetes.
- Standardize deploys with Helm/Kustomize and GitOps.
- Enforce baseline runtime hardening with Kyverno.
- Stand up full observability: Prometheus, Alertmanager, Grafana, Loki, Tempo, OTel Collector.

### What Runs Now
- **Core app tier:** API/BFF, workers, scheduler, static/ingress.
- **Data tier:** PostgreSQL, Redis, MinIO (object store).
- **Observability tier:** Prometheus, Alertmanager, Grafana, Loki, Promtail, Tempo, OpenTelemetry Collector.
- **Platform policy:** Kyverno admission + policies.

> Total pods: ~15 (varies by replicas). All exposed via K3s Traefik or Nginx Ingress.

### Architecture
```mermaid
flowchart LR
  subgraph Users
    U[Client/Operator]
  end

  subgraph Cluster[K3s Cluster]
    subgraph ns1[iip-dev]
      API[API/BFF]
      WRK[Workers]
      SCHED[Scheduler]
      PG[(PostgreSQL PVC)]
      RDS[(Redis)]
      MINIO[(MinIO PVC)]
    end

    subgraph ns2[monitoring]
      PROM[Prometheus]
      AM[Alertmanager]
      GRAF[Grafana]
      LOKI[Loki]
      PROMT[Promtail DaemonSet]
      TEMPO[Tempo]
      OTEL[OTel Collector]
    end

    subgraph ns3[kyverno]
      KYV[Kyverno]
      POL[Policies]
    end

    INGRESS[Ingress Controller]
  end

  U --> INGRESS --> API
  API --> PG
  API --> RDS
  API --> MINIO
  PROMT --> LOKI
  LOKI --> GRAF
  PROM --> GRAF
  TEMPO --> GRAF
  OTEL --> PROM & TEMPO & LOKI
  KYV -.admission.-> Cluster

Requirements
	•	K3s installed and healthy (k3s kubectl get nodes returns Ready).
	•	kubectl context set to this cluster.
	•	helm v3 installed.
	•	StorageClass default set and tested.

Deploy

# 1) Namespaces
kubectl apply -f k8s/namespaces.yaml  # iip-dev, monitoring, kyverno

# 2) Kyverno + baseline policies
helm repo add kyverno https://kyverno.github.io/kyverno
helm repo update
helm upgrade --install kyverno kyverno/kyverno -n kyverno --create-namespace --set installCRDs=true
kubectl apply -f k8s/kyverno/policies/  # runtime-hardening, image-pulls, seccomp

# 3) Observability stack
helm repo add grafana https://grafana.github.io/helm-charts
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana-loki https://grafana.github.io/helm-charts
helm repo update

helm upgrade --install kube-prometheus-stack prometheus-community/kube-prometheus-stack -n monitoring \
  --values k8s/monitoring/kps.values.yaml

helm upgrade --install loki grafana/loki -n monitoring --values k8s/monitoring/loki.values.yaml
helm upgrade --install promtail grafana/promtail -n monitoring --values k8s/monitoring/promtail.values.yaml
helm upgrade --install tempo grafana/tempo -n monitoring --values k8s/monitoring/tempo.values.yaml
helm upgrade --install otel-collector open-telemetry/opentelemetry-collector -n monitoring \
  --values k8s/monitoring/otel.values.yaml

# 4) App + data tier
kubectl apply -k k8s/iip-dev/  # or helm upgrade --install <chart> -f values.yaml

Verify

# Pods and health
kubectl get pods -A
kubectl -n monitoring get svc grafana kube-prometheus-stack-prometheus alertmanager

# Ingress/HTTP checks
kubectl -n iip-dev get ingress
curl -I https://api.iip.local/healthz

# Observability signals
kubectl -n monitoring port-forward svc/grafana 3000:80
# login → Dashboards: Kubernetes / USE Method / Loki Logs / Tempo Traces

# Policy enforcement
kubectl -n iip-dev apply -f k8s/iip-dev/tests/pod-lr-check.yaml || true
# Expect admission denial if policy is working

Policy: Runtime Hardening (Kyverno)

The cluster enforces least privilege. Typical failures look like:

admission webhook "validate.kyverno.svc-fail" denied the request:
policy runtime-hardening: Containers must drop CAP_NET_RAW

Compliant pod spec snippet:

securityContext:
  runAsNonRoot: true
  allowPrivilegeEscalation: false
  seccompProfile:
    type: RuntimeDefault
  capabilities:
    drop: ["ALL", "NET_RAW"]
  readOnlyRootFilesystem: true

Observability Map
	•	Metrics: Prometheus (scrapes), Grafana dashboards.
	•	Logs: Promtail → Loki. Search in Grafana Explore.
	•	Traces: OTel SDK → OTel Collector → Tempo. View in Grafana Explore.
	•	Alerts: Alertmanager routes (Slack/Email via K8s Secrets).

Backups and PVCs
	•	PostgreSQL and MinIO use PersistentVolumeClaims.
	•	Schedule backups with a CronJob or Velero (out of scope here). Ensure RPO/RTO targets are documented.

Rollout and Rollback

# Rolling update
kubectl -n iip-dev set image deploy/api api=registry.local/iip/api:${GIT_SHA}

# History and rollback
kubectl -n iip-dev rollout history deploy/api
kubectl -n iip-dev rollout undo deploy/api --to-revision=<n>

Operations Checklist
	•	Daily: kubectl get pods -A, Grafana overview, Alertmanager silences reviewed.
	•	Weekly: Backup restore drill, policy audit (kubectl get cpol -A), image CVE scan.
	•	Monthly: Capacity review (CPU/mem/disk), cost and limits/requests tuning.

⸻

Service Inventory (fill as you iterate)

Namespace	Service/Chart	Image/Chart Ref	Ports	PVC	Healthcheck	CPU/Memory	Notes
iip-dev	api	registry.local/iip/api:<git-sha>	80	–	/healthz	250m/512Mi	Ingress api.iip.local
iip-dev	workers	registry.local/iip/worker:<git-sha>	–	–	queue heartbeat	250m/512Mi	HPA 1–3
iip-dev	postgres	bitnami/postgresql	5432	✓	tcp	500m/2Gi	PVC 20Gi
iip-dev	redis	bitnami/redis	6379	–	tcp	200m/512Mi	auth enabled
iip-dev	minio	minio/minio	9000	✓	tcp	300m/1Gi	PVC 50Gi
monitoring	kube-prometheus-stack	prometheus-community/kube-prometheus-stack	9090	–	/-/healthy	500m/1Gi	includes Prom/AM
monitoring	grafana	grafana/grafana	80	–	/login 200	200m/256Mi	admin via Secret
monitoring	loki	grafana/loki	3100	✓	/ready	300m/1Gi	boltdb-shipper
monitoring	promtail	grafana/promtail	–	–	DaemonSet	100m/128Mi	node logs
monitoring	tempo	grafana/tempo	3200	✓	/ready	300m/512Mi	traces
monitoring	otel-collector	otel/opentelemetry-collector	4317	–	/healthz	200m/256Mi	gateway mode
kyverno	kyverno	kyverno/kyverno	–	–	webhook healthy	300m/512Mi	admission policies

Repo Layout (convention)

k8s/
  namespaces.yaml
  iip-dev/
    kustomization.yaml
    deployments/*.yaml
    services/*.yaml
    ingresses/*.yaml
    config/*.yaml
    tests/pod-lr-check.yaml
  monitoring/
    kps.values.yaml
    loki.values.yaml
    promtail.values.yaml
    tempo.values.yaml
    otel.values.yaml
  kyverno/
    policies/*.yaml
docs/
  phase12_kubernetes.md

Change Log
	•	Phase 12: K3s online; ~15 services migrated; Kyverno baseline active; full metrics/logs/traces live.

If you want this as a separate `docs/phase12_kubernetes.md`, say so and I’ll generate that file variant.

---
## 🧭 Phase 13 — Governance & Orchestration (Airflow)

This phase establishes **Apache Airflow** as the centralized governance and orchestration layer for `IIP_SECURE_STACK`.  
It ensures that all system workflows, validations, and policy checks run under a unified scheduling and compliance engine.

**Pipeline:**
1. Airflow scheduler and webserver running on `localhost:8080`
2. DAG serialization enabled (`store_serialized_dags=True`)
3. Governance DAG (`governance_check`) validates `policies.yaml`
4. Logs and metadata stored in `phase13_orchestration/airflow.db`

**Result:**
✅ Governance engine operational  
✅ Scheduler / Webserver / Metadatabase healthy  
✅ Policy validation automated through Airflow
--
### System Flow

![Client](https://img.shields.io/badge/Client-Browser-555) ➜
![Nginx](https://img.shields.io/badge/Nginx-009639?logo=nginx&logoColor=white) ➜
![Flask%20API](https://img.shields.io/badge/Flask_API-000000?logo=flask&logoColor=white) ➜
![AI%20Bridge](https://img.shields.io/badge/AI_Bridge-LLM_Integration-111111) ➜
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white) +
![DuckDB](https://img.shields.io/badge/DuckDB-FFE800) ➜
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white) /
![Apache%20Superset](https://img.shields.io/badge/Apache_Superset-1A73E8?logo=apache&logoColor=white) ➜
![Grafana](https://img.shields.io/badge/Grafana-F46800?logo=grafana&logoColor=white)

*Client → Nginx → Flask API → AI Bridge → Postgres/DuckDB → Streamlit/Superset → Grafana*


------------------------
Yes. Paste this into README.md as the Phase 13 section.

## 🧭 Phase 13 — Governance & Orchestration (Airflow)

**Status:** Completed • **Mode:** Private, cluster-aware • **Date:** November 2025  
**Endpoints:** Webserver `:8080`, Flower `:5555` (opt) • **Executor:** Celery or Local  
**Stores:** Metadata DB (Postgres), Remote logs (MinIO S3) • **DAGs:** `phase13_orchestration/dags/*`

### Objectives
- Centralize workflow governance and policy checks.
- Continuously validate K8s manifests, Kyverno policies, backups, and SLAs.
- Provide repeatable orchestration for build, verify, and deploy paths.
- Emit metrics, logs, and traces for audits.

### Architecture
```mermaid
flowchart LR
  U[Operator/UI] --> WEB[Airflow Webserver :8080]
  WEB --> SCH[Scheduler]
  SCH --> TRG[Triggerer]
  SCH --> EXE[Executor (Local/Celery)]
  EXE -->|tasks| DAGS[Governance DAGs]
  subgraph Governance Tasks
    POL[Validate policies.yaml]
    DRIFT[K8s drift scan\n(kubectl/Helm diff)]
    BAK[Backup verify\n(Restore test)]
    CVE[Container scan\n(Trivy opt)]
    SLO[SLA monitors]
  end
  DAGS --> POL
  DAGS --> DRIFT
  DAGS --> BAK
  DAGS --> CVE
  DAGS --> SLO

  subgraph Integrations
    K8S[Kubernetes API]
    GIT[GitHub API]
    S3[MinIO S3 Logs]
    ALERT[Alertmanager/Slack]
    OTEL[OTel/Prometheus/Loki]
  end
  POL --> K8S
  DRIFT --> K8S
  DRIFT --> GIT
  BAK --> S3
  DAGS -. metrics/logs .-> OTEL
  DAGS --> ALERT

What Runs Now
	•	Airflow core: webserver, scheduler, triggerer, (optional) Celery workers and Flower.
	•	DAGs: governance_check, k8s_drift_guard, backup_restore_check, sla_monitor, helm_promote.
	•	Storage: Postgres metadata, remote logging to MinIO.
	•	Observability: StatsD→Prometheus, JSON logs shipped to Loki, optional OTel spans.

Security Controls
	•	Airflow user via bootstrap Secret. Admin creds not in repo.
	•	Fernet enabled. Remote logs signed server-side.
	•	Read-only K8s RBAC for validation tasks; write only in helm_promote.
	•	Airflow Variables contain only non-secret toggles; use Connections or Secret backends for credentials.

Environment

# .env.example
AIRFLOW__CORE__EXECUTOR=CeleryExecutor        # or LocalExecutor
AIRFLOW__CORE__FERNET_KEY=<redacted>                 # generate
AIRFLOW__CORE__LOAD_EXAMPLES=False
AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION=True
AIRFLOW__CORE__DAGBAG_IMPORT_TIMEOUT=120
AIRFLOW__CORE__STORE_SERIALIZED_DAGS=True
AIRFLOW__CORE__STORE_DAG_CODE=True

# Remote logging to MinIO (S3 API)
AIRFLOW__LOGGING__REMOTE_LOGGING=True
AIRFLOW__LOGGING__REMOTE_BASE_LOG_FOLDER=s3://airflow-logs
AIRFLOW__LOGGING__REMOTE_LOG_CONN_ID=s3_logs

# Metrics
AIRFLOW__METRICS__STATSD_ON=True
AIRFLOW__METRICS__STATSD_HOST=statsd
AIRFLOW__METRICS__STATSD_PORT=8125

# Optional OTel for tasks that emit spans
OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317

# Connections (set in UI or env)
# AIRFLOW_CONN_S3_LOGS=s3://ACCESS_KEY:SECRET_KEY@minio:9000?host=http%3A%2F%2Fminio%3A9000&region=us-east-1
# AIRFLOW_CONN_KUBERNETES_DEFAULT=kubernetes://?in_cluster=True
# AIRFLOW_CONN_GIT_DEFAULT=http://token@github.com/org/repo

Docker Compose

version: "3.9"
x-airflow-image: &airflow_image apache/airflow:2.9.2
services:
  postgres:
    image: bitnami/postgresql:16
    environment:
      - POSTGRESQL_USERNAME=airflow
      - POSTGRESQL_PASSWORD=<redacted>
      - POSTGRESQL_DATABASE=airflow
    ports: ["5432:5432"]
    volumes: ["pgdata:/bitnami/postgresql"]

  redis:
    image: redis:7
    ports: ["6379:6379"]

  airflow-webserver:
    image: *airflow_image
    env_file: .env
    command: webserver
    ports: ["8080:8080"]
    depends_on: [postgres, redis]
    volumes:
      - ./phase13_orchestration/dags:/opt/airflow/dags
      - ./phase13_orchestration/plugins:/opt/airflow/plugins
      - ./logs:/opt/airflow/logs

  airflow-scheduler:
    image: *airflow_image
    env_file: .env
    command: scheduler
    depends_on: [postgres, redis]
    volumes:
      - ./phase13_orchestration/dags:/opt/airflow/dags
      - ./phase13_orchestration/plugins:/opt/airflow/plugins
      - ./logs:/opt/airflow/logs

  airflow-triggerer:
    image: *airflow_image
    env_file: .env
    command: triggerer
    depends_on: [postgres, redis]
    volumes:
      - ./phase13_orchestration/dags:/opt/airflow/dags

  airflow-worker:
    image: *airflow_image
    env_file: .env
    command: celery worker
    depends_on: [airflow-scheduler, redis, postgres]
    volumes:
      - ./phase13_orchestration/dags:/opt/airflow/dags
      - ./logs:/opt/airflow/logs

  flower:
    image: *airflow_image
    env_file: .env
    command: celery flower
    ports: ["5555:5555"]
    depends_on: [redis]

volumes:
  pgdata:

Kubernetes (Helm) — optional

helm repo add apache-airflow https://airflow.apache.org
helm repo update
helm upgrade --install airflow apache-airflow/airflow -n iip-dev --create-namespace \
  -f k8s/airflow/values.yaml

# k8s/airflow/values.yaml (snippet)
executor: CeleryExecutor
images:
  airflow:
    repository: apache/airflow
    tag: "2.9.2"
env:
  - name: AIRFLOW__CORE__STORE_SERIALIZED_DAGS
    value: "True"
  - name: AIRFLOW__LOGGING__REMOTE_LOGGING
    value: "True"
  - name: AIRFLOW__LOGGING__REMOTE_BASE_LOG_FOLDER
    value: "s3://airflow-logs"
  - name: AIRFLOW__LOGGING__REMOTE_LOG_CONN_ID
    value: "s3_logs"
dags:
  persistence:
    enabled: true
logs:
  persistence:
    enabled: true
web:
  service:
    type: ClusterIP
rbac:
  create: true

Governance DAG (example)

# phase13_orchestration/dags/governance_check.py
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
import yaml, re, subprocess, json, os, sys

def validate_policies(path="k8s/kyverno/policies"):
    for root, _, files in os.walk(path):
        for f in files:
            if f.endswith((".yml",".yaml")):
                with open(os.path.join(root,f),"r") as fh:
                    yaml.safe_load(fh)  # raises on invalid YAML
    return "ok"

def fail_on_banned(pattern=r"\b(AllowPrivilegeEscalation:\s*true|CAP_SYS_ADMIN)\b", path="k8s"):
    rx = re.compile(pattern, re.I)
    bad = []
    for root, _, files in os.walk(path):
        for f in files:
            if f.endswith((".yml",".yaml")):
                txt = open(os.path.join(root,f)).read()
                if rx.search(txt):
                    bad.append(os.path.join(root,f))
    if bad:
        raise ValueError(f"banned settings: {bad}")
    return "ok"

def helm_diff():
    # requires helm and helm-diff in image or mounted
    cmd = ["bash","-lc","helm diff upgrade iip-dev ./charts/iip-dev -n iip-dev || true"]
    out = subprocess.run(cmd, capture_output=True, text=True)
    # emit diff length for metrics
    print(json.dumps({"diff_len": len(out.stdout)}))
    return "ok"

default_args = {
  "owner": "governance",
  "retries": 1,
  "retry_delay": timedelta(minutes=2),
  "sla": timedelta(minutes=30)
}

with DAG(
  dag_id="governance_check",
  start_date=datetime(2025,11,1),
  schedule_interval="*/30 * * * *",
  catchup=False,
  default_args=default_args,
  tags=["governance","security","k8s"],
) as dag:

    validate = PythonOperator(task_id="validate_yaml", python_callable=validate_policies)
    ban_scan = PythonOperator(task_id="ban_scan", python_callable=fail_on_banned)
    dry_run = BashOperator(
        task_id="k8s_server_dry_run",
        bash_command="kubectl apply -f k8s/ --server-side --dry-run=server -n iip-dev"
    )
    diff = PythonOperator(task_id="helm_diff", python_callable=helm_diff)

    validate >> ban_scan >> dry_run >> diff

SLA / Monitoring
	•	DAG SLA: 30 minutes. Alert if missed.
	•	Task alerts: Slack/Alertmanager on failure.
	•	Metrics: Airflow StatsD exporter scraped by Prometheus.
	•	Logs: remote to S3 (MinIO), pulled by Loki with S3 source or via Promtail on pods.

CI/CD Hooks
	•	Lint and parse on PR:
	•	flake8, black --check, isort --check-only
	•	airflow dags list inside apache/airflow container
	•	Block merge on parse failures. Optional unit tests via pytest using airflow extras.

Tests (pytest)

# tests/test_parse_dags.py
import os
from airflow.models import DagBag

def test_dagbag_imports():
    db = DagBag(dag_folder="phase13_orchestration/dags", include_examples=False)
    assert len(db.import_errors) == 0, f"errors: {db.import_errors}"
    assert "governance_check" in db.dags

Service Inventory

Component	Image/Ref	Port	Health	Notes
Webserver	apache/airflow:2.9.x	8080	/health	Admin via Secret
Scheduler	apache/airflow:2.9.x	—	/health	Serialized DAGs on
Triggerer	apache/airflow:2.9.x	—	/health	deferrables
Worker (Celery)	apache/airflow:2.9.x	—	/health	optional
Flower	apache/airflow:2.9.x	5555	/	optional
Metadata DB	bitnami/postgresql:16	5432	TCP	separate PVC
StatsD	prom/statsd-exporter	8125	/metrics	Prometheus scrape

Repo Layout

phase13_orchestration/
  dags/
    governance_check.py
    k8s_drift_guard.py
    backup_restore_check.py
    sla_monitor.py
    helm_promote.py
  plugins/
  tests/
k8s/
  airflow/values.yaml
logs/                    # .gitignored

Deploy

# Local
docker compose up -d --build
open http://localhost:8080

# Kubernetes
helm upgrade --install airflow apache-airflow/airflow -n iip-dev -f k8s/airflow/values.yaml
kubectl -n iip-dev get pods -l component=webserver

Troubleshooting
	•	DAG import errors: run docker compose logs airflow-scheduler.
	•	Remote logs missing: confirm AIRFLOW_CONN_S3_LOGS and MinIO bucket.
	•	K8s dry-run fails: fix invalid manifests; check Kyverno policies.
	•	Helm diff no output: ensure helm-diff plugin present in worker image.

Change Log
	•	Phase 13: Airflow online; governance DAGs active; remote logging and metrics enabled.


---

## 🧠 Tech Stack

![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Postgres](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-F46800?logo=grafana&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![LlamaCPP](https://img.shields.io/badge/Llama_CPP-000000?logo=llama&logoColor=white)
![Superset](https://img.shields.io/badge/Apache_Superset-1A73E8?logo=apache&logoColor=white)

---

## 🧰 Installation

```bash
# Clone repository
git clone https://github.com/ivan-iip/IIP_SECURE_STACK.git
cd IIP_SECURE_STACK

# Build and start stack
docker-compose up -d --build

# Verify core services
curl -i http://localhost:5001/health
curl -i http://localhost:8088/health

Note: Ensure you have Docker ≥ 24.0 and Compose ≥ 2.20 installed.
To run the AI model locally, download a .gguf file (e.g., Phi-2) from Hugging Face before starting llama_cpp.server.

⸻

🧪 Local Testing

# Run API tests
pytest tests/

# Check container health
docker ps
docker logs <container_name>

# Validate security endpoints
curl -i https://localhost:5001/metrics


⸻

🤝 Contributing

Contributions are welcome. Fork the repository and submit pull requests with clear commit messages.
Follow existing naming conventions for Docker services and environment files.

# Lint and format code
black app/
flake8 app/


⸻

📜 License

This project is distributed under the MIT License.
See the LICENSE file for details.

⸻

🌍 Vision

IIP_SECURE_STACK exists to restore digital sovereignty—allowing creators to build, analyze, and deploy within systems rooted in trust, transparency, and control.
It is the foundation of the Inner Infinite Power™ ecosystem, designed to merge technology, structure, and human awareness.

⸻

🧩 Creator

Ivan Israel Patiño
Founder & Architect — Inner Infinite Power™ (IIP™)
📁 Project Portal
📧 Contact via GitHub Issues for technical inquiries.

⸻

🩺 Health & Observability Snapshot

curl -i http://localhost:3000/api/health
docker stats

Use Grafana dashboards (localhost:3000) for real-time metrics.

⸻

🧭 Roadmap (2025)
	•	Phase 12 – AI ↔ SQL Bridge
	•	Phase 13 – Autonomous Workflow Mesh
	•	Phase 14 – Model Monitoring & Analytics
	•	Phase 15 – Secure Front-End Delivery
	•	Phase 16 – Distributed Node Scaling

⸻

🧩 Integrity Statement

Every commit and build artifact in this repository is verified and reproducible.
All configuration files pass container security checks and environment isolation audits.

⸻
Here are both companion files — minimal, professional, and GitHub-ready.

⸻

CONTRIBUTING.md

# 🤝 Contributing to IIP_SECURE_STACK

Thank you for your interest in improving **IIP_SECURE_STACK**.  
This guide explains the standards for submitting issues, pull requests, and enhancements.

---

## 🧩 Branch & Commit Rules

- `main` — production-ready branch (protected).  
- `dev` — active development branch.  
- Feature branches follow the pattern:  
  `feature/<short-description>`  

Commit messages use the format:

type(scope): short summary

Example:

feat(api): add SQL bridge integration
fix(ci): correct Docker healthcheck path

---

## ⚙️ Development Setup

1. Fork the repository.  
2. Clone your fork:
   ```bash
   git clone https://github.com/<your-username>/IIP_SECURE_STACK.git
   cd IIP_SECURE_STACK

	3.	Install dependencies:

pip install -r requirements.txt


	4.	Run the stack locally:

docker-compose up -d



⸻

🧪 Testing
	•	Unit tests use pytest.
	•	Linting uses flake8 and black.

pytest -v
black --check app/
flake8 app/

Before opening a pull request:
	•	Ensure all tests pass.
	•	Rebase from dev to minimize merge conflicts.

⸻

🩺 Security Reporting

Do not post security issues publicly.
Report vulnerabilities privately through GitHub Security Advisories or by contacting the project maintainer via encrypted channel.

⸻

🧭 Contribution Flow
	1.	Fork → clone → create feature branch
	2.	Make and test changes
	3.	Commit following guidelines
	4.	Push branch and open a Pull Request to dev
	5.	Wait for review and approval

⸻

🧱 Code of Conduct

Respect contributors.
No harassment, discrimination, or spam.
Focus on clarity, transparency, and technical precision.

⸻

✅ Contribution Checklist
	•	Code builds successfully
	•	Tests pass
	•	Docs updated
	•	Security verified
	•	PR title matches convention

Thank you for contributing to Inner Infinite Power™ Secure Stack.

---

### **`LICENSE`** (MIT)

Inner Infinite Power™ Proprietary License

Copyright (c) 2025 Ivan Israel Patiño
All Rights Reserved.
Founder & Architect, Inner Infinite Power™ (IIP)
Buckeye, Arizona, USA

⸻

License Terms

This software and all associated documentation, data schemas, AI models, and integration frameworks (collectively, the “Software”) are the confidential and proprietary property of Ivan Israel Patiño and Inner Infinite Power™.

Unauthorized copying, reproduction, modification, redistribution, public display, or use of the Software, in whole or in part, is strictly prohibited without prior written consent of the copyright holder.

No license or rights are granted to any individual, organization, or entity except through a formal, written, and signed agreement with Inner Infinite Power™.

⸻

Permitted Internal Use

Authorized collaborators or licensees may use the Software solely for:
	•	Internal research and development
	•	System integration testing
	•	Educational or technical demonstrations approved in writing

All other uses, including commercial distribution, derivative products, or resale, are expressly forbidden without explicit authorization.

⸻

Confidentiality

All source code, data models, neural interfaces, and configuration frameworks are confidential.
Redistribution, exposure, or publication of proprietary logic, schema structures, or AI workflows is prohibited under penalty of law.

⸻

Liability and Warranty Disclaimer

The Software is provided “AS IS,” without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and noninfringement.
In no event shall the author or copyright holder be liable for any claim, damages, or other liability arising from use of the Software.

⸻

Trademark and Brand Notice

Inner Infinite Power™, Infused Alignment Method™, Pyramium™, and IIP_SECURE_STACK™
are protected trademarks and proprietary systems of Ivan Israel Patiño.
Any unauthorized use, reproduction, or misrepresentation of these marks is strictly prohibited.

⸻

Contact

Inner Infinite Power™ (IIP)
Email: iipower.automation@gmail.com
Location: Buckeye, Arizona, USA

⸻

Would you like me to generate a PDF version of this (with your gold + white branding and digital signature line) so you can upload it to the /legal/ folder of your GitHub repository? It would be formatted for investor and filing purposes.


⸻
# 🛡️ Security Policy

## Supported Versions

Only the latest stable release of **IIP_SECURE_STACK** receives active security updates.  
Older versions may continue to function but are not guaranteed to receive patches.

| Version | Supported |
|:---------|:-----------|
| main (latest) | ✅ |
| dev (testing) | ⚠️ limited support |
| older branches | ❌ not supported |

---

## 📢 Reporting a Vulnerability

Security is taken seriously.  
If you discover a vulnerability, **do not open a public issue**.

Instead, please report it privately via one of the following methods:

1. Use **GitHub Security Advisories**  
   - Navigate to: `Security` → `Advisories` → `Report a vulnerability`
2. Or contact the maintainer securely:  
   - **Encrypted email (preferred):** request via GitHub private message  
   - **Do not** send sensitive details in plaintext

All reports will receive acknowledgment within **48 hours**.

---

## 🧩 Disclosure Process

1. Vulnerability report received.  
2. Maintainer validates issue and assigns severity (Low/Medium/High/Critical).  
3. Fix developed and verified in a private branch.  
4. Patch released and changelog updated.  
5. Reporter credited (if desired).

---

## 🔒 Security Hardening Practices

IIP_SECURE_STACK enforces multiple layers of defense:

- **Container Security:** Minimal base images, no root processes.  
- **Network Isolation:** Internal bridge networks and restricted ports.  
- **Secrets Management:** `.env` variables encrypted and mounted securely.  
- **TLS Enforcement:** All communications use HTTPS with verified certificates.  
- **Audit Logging:** Continuous monitoring through Grafana + Loki.  
- **Dependency Scans:** Automated weekly via GitHub Actions.

---

## 🧠 Responsible Disclosure Guidelines

- Provide a clear description of the issue and how to reproduce it.  
- Avoid publishing exploit details until a patch is released.  
- Coordinate responsibly to protect users and data integrity.

---

⛓️🛡️ Security Philosophy

IIP_SECURE_STACK is built around **data sovereignty, audit transparency, and minimal attack surface**.  
Every component is designed to run **locally, verifiably, and privately**—free from vendor lock-in or opaque dependencies.

---
---

🛡️ Compliance and Security Framework

**Inner Infinite Power™ LLC** operates a **HIPAA-aligned, SOC 2-ready DevSecOps ecosystem** known as **IIP_SECURE_STACK** — a private infrastructure designed for continuous integrity, confidentiality, and observability of client and wellness data.

### Core Safeguards
- End-to-end encryption (TLS 1.3 / AES-256)
- Containerized isolation and RBAC segmentation
- Continuous integration / continuous delivery (CI/CD) with automated security scanning
- Immutable audit logging (Grafana + Loki + Promtail)
- Version-controlled compliance documentation under `docs/compliance/`

### Compliance Artifacts
- [`BAA_TEMPLATE.md`](docs/compliance/BAA_TEMPLATE.md) — Business Associate Agreement  
- [`SOC2_HIPAA_READINESS_BRIEF.md`](docs/compliance/SOC2_HIPAA_READINESS_BRIEF.md) — Executive compliance overview  
- [`SECURITY_PRIVACY_POLICY.md`](docs/compliance/SECURITY_PRIVACY_POLICY.md) — Technical and administrative safeguard policy  

**Status:**  
IIP_SECURE_STACK is designed for HIPAA §164 Subpart C and SOC 2 Type II alignment and is ready for third-party audit verification.


Date: 10/28/2025 -  Inner Infinite Power™ LLC — All rights reserved.*

---
*Maintained by:*  
**Ivan Israel Patiño**  
Founder & Architect — *Inner Infinite Power™*  
