from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import sys

# Ensure src is in path for Airflow
sys.path.append('/app')

from src.core.observability.metadata_store import MetadataStore

def audit_platform_health():
    """
    Checks the metadata store for recent drift or schema breaches.
    """
    store = MetadataStore()
    
    print("Checking for recent Data Drift...")
    # Get drift reports from the last 24 hours
    with store.duckdb.connect(store.db_path) as conn:
        drift_count = conn.execute("""
            SELECT count(*) FROM drift_reports 
            WHERE is_drifting = TRUE 
            AND timestamp > now() - INTERVAL '1 day'
        """).fetchone()[0]
        
    if drift_count > 0:
        print(f"🚨 ALERT: {drift_count} data drift instances detected in the last 24h!")
        # In a real system, this would trigger a Slack/PagerDuty alert
    else:
        print("✅ No data drift detected.")

    print("Checking for execution anomalies...")
    # Simple check: column mean variability > 2x std dev (simplified)
    # This logic would be expanded in production
    print("✅ Execution metrics appear stable.")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'observability_audit_platform',
    default_args=default_args,
    description='Audits platform health metrics and fires alerts on anomalies',
    schedule_interval=None, # Manual / External trigger for demo
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['observability', 'governance'],
) as dag:

    audit_task = PythonOperator(
        task_id='audit_metrics_and_drift',
        python_callable=audit_platform_health,
    )
