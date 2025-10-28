IIP_SECURE_STACK

About

IIP_SECURE_STACK is a production-grade, AI-assisted DevSecOps and Data Intelligence Framework engineered by Ivan Israel Patiño, founder of Inner Infinite Power™ (IIP).
It powers the automation, reliability, and security foundation of the IIP™ ecosystem — merging precision computing, data integrity, and human-aligned design into one scalable infrastructure.

⸻

System Overview

Layer	Description
Infrastructure	Dockerized Python 3.14-slim base with reproducible image builds
CI/CD Engine	GitHub Actions with Black + Ruff + Pytest + Trivy validation
Code Quality	Automated formatting, linting, and testing on every push/PR
Security Automation	Dependabot + Trivy for live vulnerability detection
Version Control	Semantic versioning and signed release tags


⸻

⚙️ Technical Highlights
	•	🔁 Automated verification — lint, test, and scan gates enforced before merge
	•	🧩 Immutable pipelines — every Docker image is version-locked and reproducible
	•	🧠 Dependabot orchestration — continuous dependency patching and safety updates
	•	🪶 Lightweight runtime — python:3.14-slim base for secure, fast builds
	•	✅ Audit-ready — all commits, merges, and scans traceable for compliance

⸻

🧠 Phase 12 — AI ↔ SQL Bridge Integration

Phase 12 marks the activation of IIP_SECURE_STACK’s AI-driven data reasoning layer, completing the first closed intelligence loop between LLM and data.

Components
	•	Local LLM Server — Phi-2 GGUF model running via llama_cpp.server on port 8000
	•	Flask Bridge — bridge.py API on port 5002, linking Postgres and DuckDB to the LLM
	•	Unified .env Schema — PG_*, DUCK_PATH, LLM_* variables centralize config
	•	Verified Databases — Postgres (iip_db) and DuckDB (data/iip.duckdb) validated
	•	Natural-Language Querying — Ask questions in plain text; responses derive from live SQL results

Result
A self-contained AI data loop that can query, reason over, and summarize its own datasets locally — bridging structured data with human-level understanding.

⸻

System Diagram

flowchart TD
    A[Code Commit<br>→ Push to Main/PR] --> B[GitHub Actions CI/CD]
    B --> C[Black + Ruff + Pytest Validation]
    C --> D[Docker Build<br>Python 3.14-slim]
    D --> E[Trivy Security Scan]
    E --> F[Version Tag + Signed Release]
    F --> G[Deploy / Integration Stage]
    G --> H[Continuous Monitoring<br>Dependabot + Logs]
    H --> I[Local LLM Server ↔ Bridge ↔ Databases]

Pipeline summary:
Every commit triggers a full build-format-test-scan cycle.
If all checks pass, a verified Docker image is produced and tagged for deployment.

⸻

Tech Stack

<p align="left">
  <img src="https://img.shields.io/badge/Python-3.14-blue?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Docker-Containerized-blue?logo=docker&logoColor=white" />
  <img src="https://img.shields.io/badge/GitHub%20Actions-CI%2FCD-blue?logo=githubactions&logoColor=white" />
  <img src="https://img.shields.io/badge/Trivy-Security%20Scan-green?logo=aqua&logoColor=white" />
  <img src="https://img.shields.io/badge/Black-Formatter-black?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Ruff-Linter-orange?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Pytest-Testing-blueviolet?logo=pytest&logoColor=white" />
  <img src="https://img.shields.io/badge/Bandit-Security%20Checks-red?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/llama_cpp-Local%20LLM-lightgrey?logo=openai&logoColor=white" />
  <img src="https://img.shields.io/badge/Postgres-Database-blue?logo=postgresql&logoColor=white" />
  <img src="https://img.shields.io/badge/DuckDB-Analytics-yellow?logo=duckdb&logoColor=black" />
  <img src="https://img.shields.io/badge/Flask-Bridge-black?logo=flask&logoColor=white" />
</p>



⸻

Creator

Ivan Israel Patiño
Founder • Systems Architect • NASM-Certified Trainer • Former Correctional Officer (8 yrs)
📍 Buckeye, Arizona, USA
Inner Infinite Power™
📧 iipower.automation@gmail.com

⸻

Vision

To establish IIP_SECURE_STACK as a model of intelligent, integrity-driven automation — a living system where structure, awareness, and technology fuse to create a foundation of precision, trust, and transformation.
