import os, json, requests
from airflow.models import Variable

def notify_failure(context):
    url = Variable.get("ALERT_WEBHOOK_URL", default_var=None)
    if not url:
        print("[Alert] ALERT_WEBHOOK_URL not set; skipping notify.")
        return
    payload = {
        "event": "airflow_task_failure",
        "dag_id": context["dag"].dag_id,
        "task_id": context["task_instance"].task_id,
        "run_id": context["run_id"],
        "logical_date": str(context["logical_date"]),
        "try_number": context["ti"].try_number,
        "state": str(context["ti"].state),
    }
    try:
        r = requests.post(url, data=json.dumps(payload), headers={"Content-Type": "application/json"}, timeout=5)
        print("[Alert] Sent status", r.status_code)
    except Exception as e:
        print("[Alert] Error sending alert:", e)
