import pandas as pd
import pytest
from src.iot.transform_iot import transform_iot_telemetry

def test_iot_transform_standard_contract():
    """Test that transformation enforces the lowercase contract and derives ingested_at."""
    raw_data = {
        "device_id": ["DEV-01"],
        "reading_ts": ["2026-03-01 12:00:00"],
        "METRIC": ["temp_c"],
        "Value": ["25.5"],
        "UNIT": ["C"],
        "_partner_marker": ["test_api"]
    }
    df = pd.DataFrame(raw_data)
    
    transformed = transform_iot_telemetry(df)
    
    # Check column names
    expected_cols = ["partner_id", "device_id", "reading_ts", "metric", "value", "unit", "ingested_at"]
    assert list(transformed.columns) == expected_cols
    
    # Check types
    assert pd.api.types.is_float_dtype(transformed["value"])
    assert pd.api.types.is_datetime64tz_dtype(transformed["reading_ts"])
    
    # Check mapping
    assert transformed["partner_id"].iloc[0] == "test_api"

def test_iot_transform_handles_garbage_timestamps():
    """Test that unparseable timestamps become NaT."""
    raw_data = {
        "device_id": ["DEV-01"],
        "reading_ts": ["NOT_A_TIME"],
        "metric": ["temp_c"],
        "value": [25.0],
        "unit": ["C"]
    }
    df = pd.DataFrame(raw_data)
    transformed = transform_iot_telemetry(df)
    
    assert pd.isna(transformed["reading_ts"].iloc[0])

def test_iot_transform_handles_missing_columns():
    """Test that missing required columns are handled and converted to NaT."""
    raw_data = {
        "device_id": ["DEV-01"],
        "metric": ["temp_c"]
    }
    df = pd.DataFrame(raw_data)
    transformed = transform_iot_telemetry(df)
    
    assert "reading_ts" in transformed.columns
    assert pd.isna(transformed["reading_ts"].iloc[0])
