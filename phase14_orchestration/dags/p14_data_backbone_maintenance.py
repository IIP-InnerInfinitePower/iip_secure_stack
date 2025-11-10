from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'iip_system',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='p14_data_backbone_maintenance',
    default_args=default_args,
    schedule='@daily',
    start_date=datetime(2025, 10, 30),
    catchup=False,
    tags=['phase14', 'data_backbone'],
) as dag:

    vacuum_postgres = BashOperator(
        task_id='vacuum_postgres',
        bash_command='psql $POSTGRES_CONN -c "VACUUM;"'
    )

    backup_postgres = BashOperator(
        task_id='backup_postgres',
        bash_command='pg_dump $POSTGRES_DB > ~/IIP_SECURE_STACK/backups/postgres_$(date +%F).sql'
    )

    integrity_check = BashOperator(
        task_id='integrity_check',
        bash_command='psql $POSTGRES_CONN -c "SELECT now();"'
    )

    vacuum_postgres >> backup_postgres >> integrity_check
