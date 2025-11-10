# Phase 13 – Governance & Orchestration (Airflow)

## Objective
Deploy Apache Airflow as the orchestration and governance layer for the IIP_SECURE_STACK.
Validate real-time policy enforcement using the `governance_check` DAG.

---

## Environment
```bash
conda activate airflow_env
export AIRFLOW_HOME=$HOME/IIP_SECURE_STACK/phase13_orchestration
export AIRFLOW__CORE__DAGS_FOLDER="$AIRFLOW_HOME/dags"
export AIRFLOW__CORE__STORE_SERIALIZED_DAGS=True
export AIRFLOW__WEBSERVER__WEB_SERVER_HOST=127.0.0.1
