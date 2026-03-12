"""
tests/test_iot_stream_rules.py

Unit tests for the IoT Streaming physics rules and standardization.
"""

import pytest
from src.streaming.iot_rules import PHYSICAL_BOUNDS, VALID_UNITS

def test_physical_bounds_config():
    """Verify that all core metrics have defined physical bounds."""
    assert "temp_c" in PHYSICAL_BOUNDS
    assert "humidity_pct" in PHYSICAL_BOUNDS
    assert "pressure_hpa" in PHYSICAL_BOUNDS
    
    # Check logic: Low must be less than High
    for metric, (low, high) in PHYSICAL_BOUNDS.items():
        assert low < high

def test_unit_mapping_config():
    """Verify that metrics point to standard units."""
    assert VALID_UNITS["temp_c"] == "C"
    assert VALID_UNITS["humidity_pct"] == "pct"
    assert VALID_UNITS["pressure_hpa"] == "hPa"
