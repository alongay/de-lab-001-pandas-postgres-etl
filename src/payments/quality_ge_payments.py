"""
src/quality_ge.py

Great Expectations "gate" for transformed datasets.

Enterprise notes:
- Run AFTER transform (schema/types standardized) and BEFORE load.
- Fail fast: raise if expectations fail so the ETL exits non-zero.
- Writes a compact validation artifact for audit/debugging.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

import great_expectations as ge
import pandas as pd


@dataclass(frozen=True)
class QualityGateResult:
    success: bool
    evaluated_expectations: int
    successful_expectations: int
    run_id: str
    artifact_path: str


def validate_payments_dataframe(df: pd.DataFrame, artifact_dir: str = "logs") -> QualityGateResult:
    """
    Validates a *transformed* payments dataframe with Great Expectations.
    """
    if df.empty:
        raise ValueError("Quality gate failed: dataframe is empty.")

    # GE validator
    v = ge.dataset.PandasDataset(df)

    # Expectations
    v.expect_table_columns_to_match_ordered_list([
        "partner_id",
        "txn_id",
        "account_id",
        "status",
        "amount",
        "currency",
        "txn_ts",
        "record_hash",
        "ingested_at"
    ])
    
    # Completeness
    required_cols = ["partner_id", "txn_id", "status", "amount", "currency", "txn_ts"]
    for col in required_cols:
        v.expect_column_values_to_not_be_null(col)

    # Validity
    v.expect_column_values_to_be_between("amount", min_value=0)
    v.expect_column_values_to_match_regex("currency", regex="^[A-Z]{3}$")
    v.expect_column_values_to_be_in_set(
        "status", 
        value_set=["AUTHORIZED", "CAPTURED", "REFUNDED", "DECLINED"]
    )

    # Uniqueness compound
    v.expect_compound_columns_to_be_unique(["partner_id", "txn_id"])

    result: Dict[str, Any] = v.validate()

    # Write artifact (safe: no secrets)
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    Path(artifact_dir).mkdir(parents=True, exist_ok=True)
    artifact_path = os.path.join(artifact_dir, f"ge_validation_{run_id}.json")

    compact = {
        "success": bool(result.get("success")),
        "statistics": result.get("statistics", {}),
        "meta": result.get("meta", {}),
        # keep results but avoid huge payloads; GE results are usually OK, but we keep it anyway:
        "results": result.get("results", []),
    }

    with open(artifact_path, "w", encoding="utf-8") as f:
        json.dump(compact, f, indent=2, default=str)

    stats = result.get("statistics", {}) or {}
    return QualityGateResult(
        success=bool(result.get("success")),
        evaluated_expectations=int(stats.get("evaluated_expectations", 0)),
        successful_expectations=int(stats.get("successful_expectations", 0)),
        run_id=run_id,
        artifact_path=artifact_path,
    )