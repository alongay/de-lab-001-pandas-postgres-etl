from __future__ import annotations

import os
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.sensors.filesystem import FileSensor

# Default arguments for the DAG
default_args = {
    "owner": "pde_admin",
    "depends_on_past": False,
    "start_date": datetime(2024, 3, 11),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

def notify_failure(context):
    """Mock alerting function for terminal visibility."""
    task_id = context.get('task_instance').task_id
    dag_id = context.get('task_instance').dag_id
    error_msg = str(context.get('exception') or "Unknown Error")
    
    # Run the slack_mock script
    import subprocess
    cmd = [
        "python3", "/app/scripts/monitoring/slack_mock.py",
        "--pipeline", dag_id,
        "--task", task_id,
        "--message", f"Failing with: {error_msg[:100]}..."
    ]
    subprocess.run(cmd, check=False)

with DAG(
    "payments_etl_pipeline",
    default_args=default_args,
    description="Enterprise Batch ETL for Payments (Demo 4)",
    schedule_interval=timedelta(minutes=10),
    catchup=False,
    tags=["demo", "payments", "batch"],
    on_failure_callback=notify_failure,
) as dag:

    # 1. Wait for Inbound Data (CSV sensor)
    # Note: sensor path is relative to /opt/airflow/dags by default or needs full path
    # In our docker-compose, the repo is at /app
    wait_for_csv = FileSensor(
        task_id="wait_for_csv_data",
        filepath="/app/data/payments/transactions_daily.csv",
        poke_interval=30,  # Check every 30 seconds
        timeout=600,       # Timeout after 10 minutes
    )

    # 2. Run the Payments ETL Pipeline
    run_payments_etl = BashOperator(
        task_id="run_payments_etl",
        bash_command="cd /app && python3 -m src.payments.etl_run_payments",
        env={
            "PYTHONPATH": "/app",
            "INGEST_SOURCE": "both",
            **os.environ
        }
    )

    # 3. Verify GE Artifacts (Governance Check)
    verify_data_quality = BashOperator(
        task_id="verify_data_quality",
        # Check if a GE validation report was created today in the logs directory
        bash_command=f"ls /app/logs/validation_results_*.json",
    )

    # Set dependencies
    wait_for_csv >> run_payments_etl >> verify_data_quality
