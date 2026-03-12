"""
src/streaming/iot_rules.py

Centralized rules and schema definitions for the IoT Streaming platform.
Reuses the contract from Demo 2 to tell a continuous story.
"""

from typing import Dict, Tuple

# === Event Model Schema ===
# This schema is used by the producer (Simulation) and Spark (Enforcement)
IOT_EVENT_SCHEMA = {
    "device_id": "string",
    "reading_ts": "timestamp",
    "metric": "string",
    "value": "double",
    "unit": "string",
    "partner_id": "string",
    "event_id": "string",
    "ingested_at": "timestamp"
}

# === Physical Realism Rules (Governance) ===
# These bounds are the "Laws of Physics" for our sensor network.
PHYSICAL_BOUNDS: Dict[str, Tuple[float, float]] = {
    "temp_c": (-40.0, 85.0),
    "humidity_pct": (0.0, 100.0),
    "pressure_hpa": (300.0, 1100.0)
}

# === Unit Mapping ===
# Validating that metrics use the correct enterprise-standard units.
VALID_UNITS: Dict[str, str] = {
    "temp_c": "C",
    "humidity_pct": "pct",
    "pressure_hpa": "hPa"
}

# === Topic Names ===
IOT_RAW_TOPIC = "iot.telemetry.raw"

# === Storage Paths ===
BRONZE_PATH = "/app/data/streaming/delta/bronze"
SILVER_PATH = "/app/data/streaming/delta/silver"
QUARANTINE_PATH = "/app/data/streaming/delta/quarantine"

# === Checkpoint Paths ===
CHECKPOINT_BRONZE = "/app/data/streaming/checkpoints/bronze"
CHECKPOINT_SILVER = "/app/data/streaming/checkpoints/silver"
