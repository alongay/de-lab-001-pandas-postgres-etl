import pandas as pd
from sqlalchemy import create_engine

from src.payments.load_payments import load_dataframe_to_postgres, LoadResult


def test_load_to_sqlite_in_memory():
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    df = pd.DataFrame(
        [
            {
                "partner_id": "api", "txn_id": "1", "status": "AUTHORIZED", 
                "amount": 10.0, "currency": "USD", 
                "txn_ts": "2026-03-01T00:00:00Z", 
                "account_id": "c1", "ingested_at": "2026-03-01T01:00:00Z",
                "record_hash": "mockhash123"
            }
        ]
    )

    r = load_dataframe_to_postgres(engine, df, table_name="raw_payments")
    assert r.rows_loaded == 1
    assert r.rows_in_table == 1