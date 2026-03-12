from __future__ import annotations

import os
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "pde_admin",
    "depends_on_past": False,
    "start_date": datetime(2024, 3, 11),
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

def notify_failure(context):
    task_id = context.get('task_instance').task_id
    dag_id = context.get('task_instance').dag_id
    error_msg = str(context.get('exception') or "Unknown Error")
    
    import subprocess
    cmd = [
        "python3", "/app/scripts/monitoring/slack_mock.py",
        "--pipeline", dag_id,
        "--task", task_id,
        "--message", f"Failing with: {error_msg[:100]}..."
    ]
    subprocess.run(cmd, check=False)

with DAG(
    "iot_batch_quality_pipeline",
    default_args=default_args,
    description="Scheduled IoT Batch Ingestion & Quality Audit (Demo 4)",
    schedule_interval="@hourly",
    catchup=False,
    tags=["demo", "iot", "batch"],
    on_failure_callback=notify_failure,
) as dag:

    # 1. Trigger IoT Batch Ingestion
    run_iot_batch = BashOperator(
        task_id="run_iot_batch",
        bash_command="cd /app && python3 -m src.iot.etl_run_iot",
        env={
            "PYTHONPATH": "/app",
            **os.environ
        }
    )

    # 2. Verify Quality Snapshot (GE artifact)
    verify_iot_quality = BashOperator(
        task_id="verify_iot_quality",
        bash_command="ls /app/logs/iot_validation_*.json",
    )

    run_iot_batch >> verify_iot_quality
