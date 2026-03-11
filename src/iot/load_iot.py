import os
import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine
from typing import Dict, Any

def load_iot_dataframe(
    engine: Engine,
    df: pd.DataFrame,
    table_name: str,
    unique_cols: list = None
) -> int:
    """
    Standard loader for IoT telemetry. 
    Uses UPSERT if unique_cols provided, otherwise appends.
    """
    if df.empty:
        return 0

    if not unique_cols:
        # Simple Append (e.g. for Quarantine)
        df.to_sql(
            name=table_name,
            con=engine,
            if_exists="append",
            index=False,
            method="multi",
            chunksize=1000
        )
        return len(df)

    staging_table = f"{table_name}_stg"
    
    # 1. Write to staging
    df.to_sql(
        name=staging_table,
        con=engine,
        if_exists="replace",
        index=False,
        method="multi",
        chunksize=1000
    )

    # 2. SQL UPSERT
    conflict_cols_str = ", ".join(unique_cols)
    update_cols = ["value", "unit", "ingested_at"]
    update_stmt = ", ".join([f"{c} = EXCLUDED.{c}" for c in update_cols])

    upsert_query = f"""
        INSERT INTO {table_name} (partner_id, device_id, reading_ts, metric, value, unit, ingested_at)
        SELECT partner_id, device_id, reading_ts, metric, value, unit, ingested_at
        FROM {staging_table}
        ON CONFLICT ({conflict_cols_str}) DO UPDATE SET
            {update_stmt};
    """

    with engine.begin() as conn:
        conn.execute(text(upsert_query))
        conn.execute(text(f"DROP TABLE IF EXISTS {staging_table};"))

    return len(df)

def partition_iot_data(df: pd.DataFrame, ge_results: Dict[str, Any]) -> Dict[str, pd.DataFrame]:
    """
    Separates the IoT DataFrame into 'clean' and 'quarantine' buckets.
    """
    if df.empty:
        return {"clean": df, "quarantine": df}
        
    # We use a mask based on the validation criteria
    clean_mask = (
        df["reading_ts"].notnull() & 
        df["value"].notnull() & 
        df["unit"].isin(["c", "pct", "hpa"])
    )
    
    # Simple bounds check for partitioning in this lab context
    temp_check = (df["metric"] == "temp_c") & (df["value"].between(-40, 85))
    hum_check = (df["metric"] == "humidity_pct") & (df["value"].between(0, 100))
    pres_check = (df["metric"] == "pressure_hpa") & (df["value"].between(300, 1100))
    
    physics_mask = temp_check | hum_check | pres_check
    final_clean_mask = clean_mask & physics_mask
    
    return {
        "clean": df[final_clean_mask].copy(),
        "quarantine": df[~final_clean_mask].copy()
    }

def load_iot_data(parts: Dict[str, pd.DataFrame], engine: Engine):
    """
    Orchestrates the loading of partitioned DataFrames.
    """
    raw_table = os.getenv("IOT_TABLE_RAW", "raw_sensor_readings")
    quarantine_table = os.getenv("IOT_TABLE_QUARANTINE", "raw_sensor_readings_quarantine")
    
    unique_keys = ["partner_id", "device_id", "reading_ts", "metric"]
    
    if not parts["clean"].empty:
        print(f"Loading {len(parts['clean'])} records to {raw_table}...")
        load_iot_dataframe(engine, parts["clean"], raw_table, unique_keys)

    if not parts["quarantine"].empty:
        print(f"Loading {len(parts['quarantine'])} records to {quarantine_table}...")
        # For quarantine, we don't necessarily need UPSERT unless we want to avoid duplicates
        load_iot_dataframe(engine, parts["quarantine"], quarantine_table, unique_keys)
