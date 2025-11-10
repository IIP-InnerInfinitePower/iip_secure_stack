from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
def hello(): print("IIP Phase 13 online")
with DAG("hello_iip", start_date=datetime(2025,10,29), schedule_interval="@daily", catchup=False) as dag:
    PythonOperator(task_id="say_hello", python_callable=hello)
