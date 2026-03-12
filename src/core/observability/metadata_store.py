import duckdb
import pandas as pd
from datetime import datetime
import os

class MetadataStore:
    """
    Handles persistence of observability metrics to a local DuckDB instance.
    """
    def __init__(self, db_path="data/observability/observability.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()

    def _init_db(self):
        with duckdb.connect(self.db_path) as conn:
            # Table for execution-level metrics
            conn.execute("""
                CREATE TABLE IF NOT EXISTS execution_metrics (
                    execution_id VARCHAR,
                    dag_id VARCHAR,
                    task_id VARCHAR,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    domain VARCHAR,
                    row_count INTEGER,
                    null_count INTEGER,
                    mean_value FLOAT,
                    std_dev FLOAT
                )
            """)
            # Table for drift detection results
            conn.execute("""
                CREATE TABLE IF NOT EXISTS drift_reports (
                    report_id VARCHAR,
                    domain VARCHAR,
                    column_name VARCHAR,
                    statistic FLOAT,
                    p_value FLOAT,
                    is_drifting BOOLEAN,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def log_metrics(self, execution_id, dag_id, task_id, domain, metrics_dict):
        """
        Logs descriptive statistics for a specific data batch.
        """
        with duckdb.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO execution_metrics 
                (execution_id, dag_id, task_id, domain, row_count, null_count, mean_value, std_dev)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                execution_id, dag_id, task_id, domain,
                metrics_dict.get('row_count'),
                metrics_dict.get('null_count'),
                metrics_dict.get('mean'),
                metrics_dict.get('std')
            ))

    def log_drift(self, domain, column_name, stat, p_val, is_drifting):
        """
        Logs the result of a Kolmogorov-Smirnov test.
        """
        report_id = f"DR_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        with duckdb.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO drift_reports 
                (report_id, domain, column_name, statistic, p_value, is_drifting)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (report_id, domain, column_name, stat, p_val, is_drifting))

    def get_historical_metrics(self, domain, limit=10):
        """
        Retrieves recent metrics for trend analysis.
        """
        with duckdb.connect(self.db_path) as conn:
            return conn.execute("""
                SELECT * FROM execution_metrics 
                WHERE domain = ? 
                ORDER BY timestamp DESC 
                LIMIT ?
            """, (domain, limit)).df()

if __name__ == "__main__":
    # Smoke test
    store = MetadataStore()
    print("DuckDB Metadata Store initialized successfully.")
    store.log_metrics("test_exec", "test_dag", "test_task", "payments", {
        "row_count": 100, "null_count": 0, "mean": 50.5, "std": 5.2
    })
    print("Logged test metrics.")
