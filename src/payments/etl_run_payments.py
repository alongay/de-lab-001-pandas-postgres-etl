from __future__ import annotations

import logging
import os
import sys
from datetime import datetime

import pandas as pd

from src.core.db import create_postgres_engine
from src.payments.extract_partner_api import extract_partner_api
from src.payments.extract_partner_csv import extract_partner_csv
from src.payments.load_payments import load_dataframe_to_postgres
from src.payments.quality_ge_payments import validate_payments_dataframe
from src.payments.transform_payments import transform_payments_dataframe

# Observability Imports
from src.core.observability.metadata_store import MetadataStore
from src.core.observability.data_drift_detector import DataDriftDetector
from src.core.observability.schema_guard import SchemaGuard


def configure_logging() -> None:
    import logging

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )


def main() -> None:
    configure_logging()
    import logging

    log = logging.getLogger("etl_run")

    engine = create_postgres_engine()
    log.info("Database engine created successfully")

    # Initialize Observability
    store = MetadataStore()
    drift_detector = DataDriftDetector()
    schema_guard = SchemaGuard()
    exec_id = os.getenv("AIRFLOW_CTX_EXECUTION_DATE", datetime.now().isoformat())

    source = os.getenv("INGEST_SOURCE", "both").lower()
    dfs = []
    
    if source in ("api", "both"):
        log.info("Extracting from API...")
        dfs.append(extract_partner_api())
        
    if source in ("csv", "both"):
        log.info("Extracting from CSV...")
        dfs.append(extract_partner_csv())

    if not dfs:
        raise ValueError(f"Invalid INGEST_SOURCE '{source}'. Must be 'api', 'csv', or 'both'.")

    df_raw = pd.concat(dfs, ignore_index=True) if len(dfs) > 1 else dfs[0]
    log.info("Extract complete: rows=%s cols=%s", df_raw.shape[0], df_raw.shape[1])

    tr = transform_payments_dataframe(df_raw)
    log.info("Transform complete: rows=%s nulls=%s", tr.row_count, tr.null_counts)
    
    gate = validate_payments_dataframe(tr.dataframe, artifact_dir="logs")
    if not gate.success:
        raise RuntimeError(
            f"Great Expectations gate failed: "
            f"{gate.successful_expectations}/{gate.evaluated_expectations} passed. "
            f"Artifact: {gate.artifact_path}"
        )
    log.info(
        "Quality gate passed: %s/%s (artifact=%s)",
        gate.successful_expectations,
        gate.evaluated_expectations,
        gate.artifact_path,
    )

    lr = load_dataframe_to_postgres(engine, tr.dataframe, table_name="raw_payments")
    log.info("Load complete: table=%s rows_loaded=%s rows_in_table=%s", lr.table_name, lr.rows_loaded, lr.rows_in_table)

    # Observability Audit
    log.info("Running Observability Audit...")
    
    # 1. Schema Check
    schema_res = schema_guard.check_schema(tr.dataframe, "payments")
    
    # 2. Drift Detection (on 'amount')
    # Cast to float for statistical analysis (Decimal is for precision in DB)
    df_obs = tr.dataframe.copy()
    df_obs["amount"] = df_obs["amount"].astype(float)
    
    drift_reports = drift_detector.detect_drift(df_obs, "payments", ["amount"])
    for report in drift_reports:
        store.log_drift("payments", report["column"], report["statistic"], report["p_value"], report["is_drifting"])
        if report["is_drifting"]:
            log.warning("🚨 DATA DRIFT DETECTED in column %s (p-value: %0.4f)", report["column"], report["p_value"])

    # 3. Log execution metrics
    metrics = {
        "row_count": int(tr.row_count),
        "null_count": int(sum(tr.null_counts.values())),
        "mean": float(df_obs["amount"].mean()),
        "std": float(df_obs["amount"].std())
    }
    store.log_metrics(exec_id, "payments_etl_pipeline", "run_payments_etl", "payments", metrics)

    log.info("Observability Audit complete. Metrics persisted to DuckDB.")
    log.info("ETL pipeline finished successfully")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        import logging
        logging.getLogger("etl_run").exception("ETL pipeline failed")
        sys.exit(1)