import pandas as pd
import pytest
from decimal import Decimal

from src.transform_payments import transform_payments_dataframe


def test_transform_api_schema():
    df_raw = pd.DataFrame(
        [
            {
                "_partner_marker": "partner_api", "txnId": "1", "status": "AUTHORIZED", 
                "amount": "10.0", "currency": "usd", 
                "txnTs": "2026-03-01T00:00:00Z"
            }
        ]
    )
    r = transform_payments_dataframe(df_raw)
    assert r.row_count == 1
    cols = set(r.dataframe.columns)
    assert {"partner_id", "txn_id", "status", "amount", "currency", "txn_ts", "account_id", "ingested_at", "record_hash"}.issubset(cols)
    assert r.dataframe["currency"].iloc[0] == "USD"
    assert pd.isna(r.dataframe["account_id"].iloc[0])
    assert isinstance(r.dataframe["amount"].iloc[0], Decimal)
    assert r.dataframe["amount"].iloc[0] == Decimal("10.00")


def test_transform_csv_schema():
    df_raw = pd.DataFrame(
        [
            {
                "_partner_marker": "partner_csv", "txn_id": "1", "status": "CAPTURED", 
                "amount": 5.0, "currency": "EUR", 
                "txn_ts": "2026-03-01T00:00:00Z"
            }
        ]
    )
    r = transform_payments_dataframe(df_raw)
    assert r.row_count == 1
    assert r.dataframe["currency"].iloc[0] == "EUR"
    assert isinstance(r.dataframe["amount"].iloc[0], Decimal)
    assert r.dataframe["amount"].iloc[0] == Decimal("5.00")
    assert r.dataframe["record_hash"].iloc[0] is not None


def test_transform_missing_marker_raises():
    df_raw = pd.DataFrame([{"txn_id": "1"}])  # missing _partner_marker
    with pytest.raises(ValueError, match="Missing _partner_marker"):
        transform_payments_dataframe(df_raw)