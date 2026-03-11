from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

import pandas as pd


@dataclass(frozen=True)
class TransformResult:
    dataframe: pd.DataFrame
    row_count: int
    null_counts: Dict[str, int]


def transform_payments_dataframe(df_raw: pd.DataFrame) -> TransformResult:
    if df_raw.empty:
        raise ValueError("Input DataFrame is empty; nothing to transform.")

    df = df_raw.copy()

    if "_partner_marker" not in df.columns:
        raise ValueError("Missing _partner_marker indicating data origin.")

    # 1. Coalesce schemas (API camelCase + CSV snake_case)
    df["partner_id"] = df["_partner_marker"]
    
    # Safely get columns, defaulting to all-null series if completely missing
    for col in ["txn_id", "txnId", "account_id", "accountId", "status", "amount", "txn_ts", "txnTs", "currency"]:
        if col not in df.columns:
            df[col] = pd.NA

    df["txn_id"] = df["txn_id"].combine_first(df["txnId"])
    df["account_id"] = df["account_id"].combine_first(df["accountId"])
    df["amount"] = df["amount"]
    df["status"] = df["status"]
    df["txn_ts"] = df["txn_ts"].combine_first(df["txnTs"])

    # 2. Select standard columns
    required_cols = {
        "partner_id", "txn_id", "status", "amount", 
        "currency", "txn_ts"
    }
    
    df = df[["partner_id", "txn_id", "account_id", "status", "amount", "currency", "txn_ts"]]

    # 3. Cast types
    df["partner_id"] = df["partner_id"].astype("string")
    df["txn_id"] = df["txn_id"].astype("string")
    df["account_id"] = df["account_id"].astype("string")
    df["status"] = df["status"].astype("string").str.upper()
    df["currency"] = df["currency"].astype("string").str.upper()
    df["txn_ts"] = pd.to_datetime(df["txn_ts"], errors="coerce")

    # Financial Precision: Decimal
    from decimal import Decimal, InvalidOperation
    def to_decimal(val) -> Decimal | None:
        if pd.isna(val):
            return None
        try:
            return Decimal(str(val))
        except InvalidOperation:
            return None
            
    df["amount"] = df["amount"].apply(to_decimal)

    # 4. Idempotency: MD5 Hash
    import hashlib
    def hash_row(row: pd.Series) -> str:
        # Create a deterministic string from core fields
        parts = [
            str(row["partner_id"]),
            str(row["txn_id"]),
            str(row["status"]),
            str(row["amount"]),
            str(row["currency"]),
            str(row["txn_ts"])
        ]
        raw_str = "|".join(parts)
        return hashlib.md5(raw_str.encode("utf-8")).hexdigest()

    df["record_hash"] = df.apply(hash_row, axis=1)

    # Add ingested_at timestamp
    df["ingested_at"] = pd.Timestamp.utcnow()

    # Null checks (minimal gate)
    null_counts = df[list(required_cols)].isna().sum().to_dict()

    return TransformResult(dataframe=df, row_count=len(df), null_counts=null_counts)
