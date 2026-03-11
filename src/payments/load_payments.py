from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine
from sqlalchemy.types import String, Numeric, DateTime


@dataclass(frozen=True)
class LoadResult:
    table_name: str
    rows_loaded: int
    rows_in_table: int


def load_dataframe_to_postgres(
    engine: Engine,
    df: pd.DataFrame,
    table_name: str = "raw_payments",
) -> LoadResult:
    if df.empty:
        raise ValueError("Refusing to load an empty DataFrame.")

    staging_table = f"{table_name}_stg"

    # Define exact schema mapping to force Postgres Data Types
    dtypes = {
        "partner_id": String(),
        "txn_id": String(),
        "account_id": String(),
        "status": String(),
        "amount": Numeric(12, 2),  # Financial precision
        "currency": String(),
        "txn_ts": DateTime(timezone=True),
        "ingested_at": DateTime(timezone=True),
        "record_hash": String()
    } if engine.dialect.name == "postgresql" else None

    # Write to staging table (commits automatically in pandas)
    df.to_sql(
        name=staging_table,
        con=engine,
        if_exists="replace",
        index=False,
        method="multi",
        chunksize=1000,
        dtype=dtypes
    )

    with engine.begin() as conn:
        # Create target table from staging schema if it doesn't exist
        # and explicitly enforce the unique constraint for upsert tracking.
        if engine.dialect.name == "postgresql":
            conn.execute(text(
                f"CREATE TABLE IF NOT EXISTS {table_name} "
                f"(LIKE {staging_table} INCLUDING ALL);"
            ))
            
            # Ensure unique constraint exists for the ON CONFLICT clause
            conn.execute(text(f"""
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1 FROM pg_constraint 
                        WHERE conrelid = '{table_name}'::regclass AND conname = '{table_name}_partner_txn_uq'
                    ) THEN
                        ALTER TABLE {table_name} ADD CONSTRAINT {table_name}_partner_txn_uq UNIQUE (partner_id, txn_id);
                    END IF;
                END $$;
            """))

            # Idempotency: UPSERT the staged data merging into production
            upsert_query = f"""
                INSERT INTO {table_name} (
                    partner_id, txn_id, account_id, status, amount, 
                    currency, txn_ts, ingested_at, record_hash
                )
                SELECT 
                    partner_id, txn_id, account_id, status, amount, 
                    currency, txn_ts, ingested_at, record_hash
                FROM {staging_table}
                ON CONFLICT (partner_id, txn_id) DO UPDATE SET
                    account_id = EXCLUDED.account_id,
                    status = EXCLUDED.status,
                    amount = EXCLUDED.amount,
                    currency = EXCLUDED.currency,
                    txn_ts = EXCLUDED.txn_ts,
                    ingested_at = EXCLUDED.ingested_at,
                    record_hash = EXCLUDED.record_hash
                WHERE {table_name}.record_hash != EXCLUDED.record_hash;
            """
            conn.execute(text(upsert_query))
        else:
            # Graceful degrade for SQLite in-memory tests (simpler replace)
            conn.execute(text(f"DROP TABLE IF EXISTS {table_name};"))
            conn.execute(text(f"CREATE TABLE {table_name} AS SELECT * FROM {staging_table};"))

        # Clean up staging table
        conn.execute(text(f"DROP TABLE IF EXISTS {staging_table};"))

    # Verify counts
    with engine.connect() as conn:
        rows_in_table = conn.execute(text(f"SELECT COUNT(*) FROM {table_name};")).scalar_one()

    return LoadResult(table_name=table_name, rows_loaded=len(df), rows_in_table=rows_in_table)
