import sys
import os
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

# Add src to path for localized utilities
sys.path.append('/opt/airflow/src')
from orchestration.platform_utils import check_delta_freshness

default_args = {
    "owner": "pde_admin",
    "depends_on_past": False,
    "start_date": datetime(2024, 3, 11),
    "retries": 0,
}

def notify_failure(context):
    task_id = context.get('task_instance').task_id
    dag_id = context.get('task_instance').dag_id
    error_msg = str(context.get('exception') or "Unknown Error")
    
    import subprocess
    cmd = [
        "python3", "/opt/airflow/scripts/monitoring/slack_mock.py",
        "--pipeline", dag_id,
        "--task", task_id,
        "--message", f"SLA Breach: {error_msg[:100]}..."
    ]
    subprocess.run(cmd, check=False)

def check_freshness(path, max_age_seconds=300):
    """Wrapper for platform_utils check_delta_freshness."""
    is_fresh, age, latest = check_delta_freshness(path, max_age_minutes=max_age_seconds/60)
    
    if not is_fresh:
        raise Exception(f"SLA Breach: Delta table {path} is stale (Age: {age:.2f}m > {max_age_seconds/60}m)")
    
    print(f"SLA OK: {path} updated {age:.2f}m ago.")

with DAG(
    "iot_stream_health_monitor",
    default_args=default_args,
    description="SLA & Freshness Monitor for IoT Streaming (Demo 4)",
    schedule_interval=timedelta(minutes=5),
    catchup=False,
    tags=["demo", "iot", "streaming", "sla"],
    on_failure_callback=notify_failure,
) as dag:

    # 1. Kafka Connectivity check
    check_kafka_pulse = BashOperator(
        task_id="check_kafka_pulse",
        # Use nc to check if Kafka is reachable on the platform network
        bash_command="nc -zv iot-kafka 9092",
    )

    # 2. Bronze Freshness Check
    check_bronze_freshness = PythonOperator(
        task_id="check_bronze_freshness",
        python_callable=check_freshness,
        op_kwargs={"path": "/opt/airflow/data/iot/delta/bronze"}
    )

    # 3. Silver Freshness Check
    check_silver_freshness = PythonOperator(
        task_id="check_silver_freshness",
        python_callable=check_freshness,
        op_kwargs={"path": "/opt/airflow/data/iot/delta/silver"}
    )

    check_kafka_pulse >> [check_bronze_freshness, check_silver_freshness]
