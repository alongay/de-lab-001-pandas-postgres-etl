from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
import sys
import os

# Ensure modular src is in path
sys.path.append('/opt/airflow/src')

default_args = {
    "owner": "hr_admin",
    "depends_on_past": False,
    "start_date": datetime(2024, 3, 11),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

def check_hr_data_exists():
    path = "/app/data/hr/inbound"
    if not os.path.exists(path) or not os.listdir(path):
        print(f"No files found in {path}")
        return False
    return True

with DAG(
    "hr_applicant_intake_dag",
    default_args=default_args,
    description="Orchestrates HR applicant intake with PII redaction and compliance gates",
    schedule_interval="@daily",
    catchup=False,
    tags=["hr", "pii", "compliance"],
) as dag:

    # 1. Sensor-like task (Python)
    validate_files = PythonOperator(
        task_id="check_inbound_data",
        python_callable=check_hr_data_exists,
    )

    # 2. Run HR ETL (Bash via ETL container or direct python if mounted)
    # Since src is mounted at /opt/airflow/src, we can run it directly if env is compatible
    # or use docker exec if airflow has access. Here we run the modular script.
    run_hr_pipeline = BashOperator(
        task_id="run_hr_pii_pipeline",
        bash_command="PYTHONPATH=/opt/airflow python3 -m src.hr.etl_run_hr",
    )

    # 3. Quality Audit (Verify Quarantine status)
    # Placeholder for a task that alerts if quarantine table grows too fast
    audit_quarantine = BashOperator(
        task_id="audit_compliance_breaches",
        bash_command="echo 'Auditing Quarantine Table for Sovereignty Breaches...'",
    )

    validate_files >> run_hr_pipeline >> audit_quarantine
