import os
import sys
import json
import pandas as pd
from datetime import datetime, timezone
from dotenv import load_dotenv
from src.core.db import create_postgres_engine
from src.iot.extract_iot import extract_iot
from src.iot.transform_iot import transform_iot_telemetry
from src.iot.quality_ge_iot import validate_iot_telemetry
from src.iot.load_iot import partition_iot_data, load_iot_data, load_iot_dataframe

def run_iot_pipeline():
    """
    Main entry point for the Demo 2 (IoT) Pipeline.
    Implements the "Quarantine Pattern": 
    If ANY validation fails, the entire batch is quarantined.
    """
    print("🚀 Initializing IoT Telemetry Pipeline (Batch Quarantine Mode)...")
    load_dotenv()
    
    # Ensure logs directory exists
    os.makedirs("logs", exist_ok=True)
    
    # 1. Extraction
    try:
        raw_df = extract_iot()
        print(f"✔️ Extracted {len(raw_df)} total records from sensors.")
    except Exception as e:
        print(f"❌ Extraction failed: {e}")
        sys.exit(1)
        
    # 2. Transformation
    clean_df = transform_iot_telemetry(raw_df)
    print("✔️ Transformation (Standard Contract & UTC) complete.")
    
    # 3. Quality Gate
    print("🔍 Running Great Expectations Quality Gate...")
    ge_results = validate_iot_telemetry(clean_df)
    success = ge_results.get("success", False)
    
    stats = ge_results.get("statistics", {})
    print(f"📊 Quality Stats: {stats.get('successful_expectations')}/{stats.get('evaluated_expectations')} expectations passed.")
    
    # 4. Persistence (Load)
    engine = create_postgres_engine()
    raw_table = os.getenv("IOT_TABLE_RAW", "raw_sensor_readings")
    quarantine_table = os.getenv("IOT_TABLE_QUARANTINE", "raw_sensor_readings_quarantine")
    
    try:
        if not success:
            print(f"⛔ QUALITY GATE FAILED! Quarantining entire batch of {len(clean_df)} records.")
            
            # Write GE result to logs
            ts_str = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
            log_path = os.path.join("logs", f"iot_quarantine_report_{ts_str}.json")
            with open(log_path, "w") as f:
                json.dump(ge_results, f, indent=2)
            print(f"📄 Validation report saved to: {log_path}")
            
            # Append entire batch to quarantine
            load_iot_dataframe(
                engine, 
                clean_df, 
                quarantine_table, 
                unique_cols=None
            )
            
            print("❌ Pipeline halted due to quality failure.")
            sys.exit(1)
        else:
            print(f"✅ Quality Gate Passed. Promoting {len(clean_df)} records to production.")
            load_iot_dataframe(
                engine, 
                clean_df, 
                raw_table, 
                unique_cols=["partner_id", "device_id", "reading_ts", "metric"]
            )
            print("🎉 Pipeline execution successful.")

    except Exception as e:
        print(f"❌ Loading failed: {e}")
        sys.exit(1)
    finally:
        engine.dispose()

if __name__ == "__main__":
    run_iot_pipeline()
