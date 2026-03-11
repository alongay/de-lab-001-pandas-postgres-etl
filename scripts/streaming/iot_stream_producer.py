"""
scripts/iot_stream_producer.py

Enterprise-grade IoT event generator for Kafka.
Simulates high-velocity telemetry (1k/sec) with controllable chaos.
"""

import json
import os
import random
import time
import uuid
from datetime import datetime, timezone
from confluent_kafka import Producer

from src.streaming.iot_rules import (
    PHYSICAL_BOUNDS, 
    VALID_UNITS, 
    IOT_RAW_TOPIC
)

# === Configuration ===
KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "iot-kafka:9092")
OUTLIER_RATE = float(os.getenv("STREAM_OUTLIER_RATE", 0.01))
BAD_UNIT_RATE = float(os.getenv("STREAM_BAD_UNIT_RATE", 0.005))
DUPLICATE_RATE = float(os.getenv("STREAM_DUPLICATE_RATE", 0.01))
EVENTS_PER_SEC = int(os.getenv("STREAM_EVENTS_PER_SEC", 100)) # Lowered for local stability but scale-ready

def delivery_report(err, msg):
    if err is not None:
        print(f"❌ Message delivery failed: {err}")

def generate_event(device_id: str, metric: str) -> dict:
    """
    Generates a realistic IoT event with occasional enterprise-grade chaos.
    """
    # 1. Base realistic value
    low, high = PHYSICAL_BOUNDS.get(metric, (0.0, 100.0))
    value = random.uniform(low, high)
    unit = VALID_UNITS.get(metric, "unknown")
    
    # 2. Inject Chaos
    roll = random.random()
    
    # Chaos: Physical Outlier (Drift or hardware failure)
    if roll < OUTLIER_RATE:
        value = 999.9  # Clear signal for the quality gate
        
    # Chaos: Unit Mismatch (Governance failure)
    elif roll < (OUTLIER_RATE + BAD_UNIT_RATE):
        unit = "Kelvin" if metric == "temp_c" else "unknown_unit"
        
    return {
        "device_id": device_id,
        "reading_ts": datetime.now(timezone.utc).isoformat(),
        "metric": metric,
        "value": round(value, 2),
        "unit": unit,
        "partner_id": "iot_streaming_inc",
        "event_id": str(uuid.uuid4()),
        "ingested_at": datetime.now(timezone.utc).isoformat()
    }

def run_producer():
    print(f"🚀 Starting IoT Stream Producer (Target: {EVENTS_PER_SEC} events/sec)", flush=True)
    print(f"📍 Target Topic: {IOT_RAW_TOPIC}", flush=True)
    print(f"📉 Chaos Levels: Outlier={OUTLIER_RATE}, BadUnit={BAD_UNIT_RATE}, Dupe={DUPLICATE_RATE}", flush=True)

    conf = {'bootstrap.servers': KAFKA_BOOTSTRAP}
    producer = Producer(conf)
    
    devices = [f"DEV-{i:04d}" for i in range(1, 11)]
    metrics = ["temp_c", "humidity_pct", "pressure_hpa"]
    
    events_sent = 0
    try:
        while True:
            # Generate event
            device = random.choice(devices)
            metric = random.choice(metrics)
            event = generate_event(device, metric)
            
            # Chaos: Duplicate delivery (Normal in distributed systems)
            if random.random() < DUPLICATE_RATE:
                producer.produce(
                    IOT_RAW_TOPIC, 
                    value=json.dumps(event).encode('utf-8'),
                    callback=delivery_report
                )
            
            # Send main event
            producer.produce(
                IOT_RAW_TOPIC, 
                value=json.dumps(event).encode('utf-8'),
                callback=delivery_report
            )
            
            events_sent += 1
            if events_sent % 100 == 0:
                print(f"✅ Sent {events_sent} events...", flush=True)
                producer.flush()
            
            # Rate limiting
            time.sleep(1.0 / EVENTS_PER_SEC)
            
    except KeyboardInterrupt:
        print("🛑 Producer stopped by user.")
    finally:
        producer.flush()

if __name__ == "__main__":
    run_producer()
