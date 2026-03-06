import pandas as pd
import pytest

from src.quality_ge_payments import validate_payments_dataframe


def test_quality_gate_passes():
    df = pd.DataFrame(
        [
            {
                "partner_id": "api", "txn_id": "1", "account_id": "c1", 
                "status": "AUTHORIZED", "amount": 10.0, "currency": "USD", 
                "txn_ts": "2026-03-01T00:00:00Z", "record_hash": "a", 
                "ingested_at": "2026-03-01T01:00:00Z"
            },
            {
                "partner_id": "csv", "txn_id": "1", "account_id": "c2", 
                "status": "CAPTURED", "amount": 5.0, "currency": "EUR", 
                "txn_ts": "2026-03-01T00:00:00Z", "record_hash": "b", 
                "ingested_at": "2026-03-01T01:00:00Z"
            },
        ]
    )
    r = validate_payments_dataframe(df, artifact_dir="logs")
    assert r.success is True


def test_quality_gate_fails_on_duplicate_partner_and_txn_id():
    df = pd.DataFrame(
        [
            {
                "partner_id": "api", "txn_id": "1", "account_id": "c1", 
                "status": "AUTHORIZED", "amount": 10.0, "currency": "USD", 
                "txn_ts": "2026-03-01T00:00:00Z", "record_hash": "a", 
                "ingested_at": "2026-03-01T01:00:00Z"
            },
            {
                "partner_id": "api", "txn_id": "1", "account_id": "c2", 
                "status": "CAPTURED", "amount": 5.0, "currency": "EUR", 
                "txn_ts": "2026-03-01T00:00:00Z", "record_hash": "b", 
                "ingested_at": "2026-03-01T01:00:00Z"
            },
        ]
    )
    r = validate_payments_dataframe(df, artifact_dir="logs")
    assert r.success is False