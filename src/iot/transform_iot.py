import pandas as pd
import numpy as np
from datetime import datetime, timezone

def transform_iot_telemetry(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardizes IoT telemetry to the production contract:
    - Enforces Lowercase Columns
    - Maps _partner_marker to partner_id
    - Casts reading_ts to UTC Datetime
    - Coerces value to Float
    - Derives ingested_at (Record creation time)
    """
    if df.empty:
        return df
        
    # 1. Column Normalization (Lowercase)
    df.columns = [c.lower() for c in df.columns]

    # 2. Defensive Initialization: Ensure required columns exist for processing
    contract_cols = ["partner_id", "device_id", "reading_ts", "metric", "value", "unit", "ingested_at"]
    for col in contract_cols:
        if col not in df.columns:
            df[col] = None
    
    # 3. Map Partner ID (Internal Marker -> Public Column)
    if "_partner_marker" in df.columns:
        df["partner_id"] = df["_partner_marker"]
    
    # 4. Timestamp Standardization (Ensure UTC awareness)
    df["reading_ts"] = pd.to_datetime(df["reading_ts"], errors='coerce', utc=True)
    
    # 5. Type Enforcement (Numeric Coercion)
    df["value"] = pd.to_numeric(df["value"], errors='coerce')
    
    # 6. Metadata Derivation (Lineage & Audit)
    df["ingested_at"] = datetime.now(timezone.utc)
    
    # 7. Final Selection & Ordering (Symmetry with DB Table)
    return df[contract_cols]
