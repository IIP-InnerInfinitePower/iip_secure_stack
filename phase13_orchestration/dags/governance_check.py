from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable
import yaml, pathlib
from alerting import notify_failure

default_args = {
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
    "on_failure_callback": notify_failure,
}

def check_policies():
    p = pathlib.Path(Variable.get("GOVERNANCE_POLICIES_PATH"))
    data = yaml.safe_load(p.read_text())
    print("[Governance] Using:", p)
    print("[Governance] Policy:", data)
    assert data["access"]["secrets"] == "deny", "Secrets access must be 'deny'."
    assert data["security"]["tls_required"] is True, "TLS must be required."
    assert data["security"]["api_keys_required"] is True, "API keys must be required."

with DAG(
    "governance_check",
    start_date=datetime(2025,10,29),
    schedule_interval="@daily",
    catchup=False,
    default_args=default_args,
) as dag:
    PythonOperator(task_id="validate_policies", python_callable=check_policies)
