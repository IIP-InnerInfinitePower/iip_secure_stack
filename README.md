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


Observability Map
	•	Metrics: Prometheus (scrapes), Grafana dashboards.
	•	Logs: Promtail → Loki. Search in Grafana Explore.
	•	Traces: OTel SDK → OTel Collector → Tempo. View in Grafana Explore.
	•	Alerts: Alertmanager routes (Slack/Email via K8s Secrets).

Backups and PVCs
	•	PostgreSQL and MinIO use PersistentVolumeClaims.
	•	Schedule backups with a CronJob or Velero (out of scope here). Ensure RPO/RTO targets are documented.


Operations Checklist
	•	Daily: kubectl get pods -A, Grafana overview, Alertmanager silences reviewed.
	•	Weekly: Backup restore drill, policy audit (kubectl get cpol -A), image CVE scan.
	•	Monthly: Capacity review (CPU/mem/disk), cost and limits/requests tuning.


Change Log
	•	Phase 12: K3s online; ~15 services migrated; Kyverno baseline active; full metrics/logs/traces live.
	
-------------------------------

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
### System Flow (2.0) 

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
-------------------------------------------------------------

### System Flow (v3.011)

#### Request/Data Path
![Client](https://img.shields.io/badge/Client-Browser-555) ➜
![Ingress](https://img.shields.io/badge/Ingress-Traefik%2FNginx-0aa) ➜
![Flask](https://img.shields.io/badge/API-Flask%2FGunicorn-000?logo=flask&logoColor=white) ➜
![AI%20Bridge](https://img.shields.io/badge/AI_Bridge-llama.cpp_server-111111) ➜
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white) +
![DuckDB](https://img.shields.io/badge/DuckDB-FFE800) +
![MinIO](https://img.shields.io/badge/Object_Storage-MinIO_S3-dd1177) ➜
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white) /
![Apache%20Superset](https://img.shields.io/badge/Apache_Superset-1A73E8) ➜
![Grafana](https://img.shields.io/badge/Grafana-F46800?logo=grafana&logoColor=white)

#### Control/Observability Path
![GitHub%20Actions](https://img.shields.io/badge/CI-GitHub_Actions-2f80ed?logo=githubactions&logoColor=white) ➜
![GHCR](https://img.shields.io/badge/Registry-GHCR-24292e?logo=github&logoColor=white) ➜
![K3s](https://img.shields.io/badge/Runtime-K3s-ffc107) •
![Airflow](https://img.shields.io/badge/Governance-Airflow-017CEE?logo=apacheairflow&logoColor=white) ➜ K8s API •
![Kyverno](https://img.shields.io/badge/Policy-Kyverno-1c7ed6) (admission) •
![OTel](https://img.shields.io/badge/OTel-Collector-6c43f3) ➜
![Prometheus](https://img.shields.io/badge/Metrics-Prometheus-E6522C?logo=prometheus&logoColor=white) |
![Loki](https://img.shields.io/badge/Logs-Loki-00a37a) |
![Tempo](https://img.shields.io/badge/Traces-Tempo-3b82f6) ➜
![Grafana](https://img.shields.io/badge/Views-Grafana-F46800?logo=grafana&logoColor=white)

---



------------------------

## 🧭 Phase 13 — Governance & Orchestration (Airflow)

**Status:** Completed • **Mode:** Private, cluster-aware • **Date:** November 2025  
**Endpoints:** Webserver `:8080`, Flower `:5555` (opt) • **Executor:** Celery or Local  
**Stores:** Metadata DB (Postgres), Remote logs (MinIO S3) • **DAGs:** `phase13_orchestration/dags/*`

### Objectives
- Centralize workflow governance and policy checks.
- Continuously validate K8s manifests, Kyverno policies, backups, and SLAs.
- Provide repeatable orchestration for build, verify, and deploy paths.
- Emit metrics, logs, and traces for audits.



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
