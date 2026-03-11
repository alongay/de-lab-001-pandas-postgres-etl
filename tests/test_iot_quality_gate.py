import pandas as pd
import pytest
import json
from src.iot.quality_ge_iot import validate_iot_telemetry

def test_quality_gate_valid_batch():
    """Test that a physically valid batch passes."""
    data = {
        "partner_id": ["api"],
        "device_id": ["DEV-01"],
        "reading_ts": [pd.Timestamp("2026-03-01", tz="UTC")],
        "metric": ["temp_c"],
        "value": [25.0],
        "unit": ["c"],
        "ingested_at": [pd.Timestamp.now(tz="UTC")]
    }
    df = pd.DataFrame(data)
    results = validate_iot_telemetry(df)
    assert results["success"] is True

def test_quality_gate_humidity_overflow():
    """Test that humidity > 100 fails."""
    data = {
        "partner_id": ["api"],
        "device_id": ["DEV-01"],
        "reading_ts": [pd.Timestamp("2026-03-01", tz="UTC")],
        "metric": ["humidity_pct"],
        "value": [150.0],
        "unit": ["pct"],
        "ingested_at": [pd.Timestamp.now(tz="UTC")]
    }
    df = pd.DataFrame(data)
    results = validate_iot_telemetry(df)
    assert results["success"] is False

def test_quality_gate_wrong_unit():
    """Test that temp_c with unit F fails."""
    data = {
        "partner_id": ["api"],
        "device_id": ["DEV-01"],
        "reading_ts": [pd.Timestamp("2026-03-01", tz="UTC")],
        "metric": ["temp_c"],
        "value": [25.0],
        "unit": ["f"], # Chaos!
        "ingested_at": [pd.Timestamp.now(tz="UTC")]
    }
    df = pd.DataFrame(data)
    results = validate_iot_telemetry(df)
    assert results["success"] is False

def test_quality_gate_duplicate_keys():
    """Test that non-unique compound keys fail."""
    ts = pd.Timestamp("2026-03-01", tz="UTC")
    data = {
        "partner_id": ["api", "api"],
        "device_id": ["DEV-01", "DEV-01"],
        "reading_ts": [ts, ts],
        "metric": ["temp_c", "temp_c"],
        "value": [25.0, 26.0],
        "unit": ["c", "c"],
        "ingested_at": [pd.Timestamp.now(tz="UTC"), pd.Timestamp.now(tz="UTC")]
    }
    df = pd.DataFrame(data)
    results = validate_iot_telemetry(df)
    assert results["success"] is False
