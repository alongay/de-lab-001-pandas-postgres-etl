import duckdb
import pandas as pd
import sys
import os

def main():
    db_path = "/app/data/observability/observability.db"
    if not os.path.exists(db_path):
        print(f"Error: Metadata store not found at {db_path}")
        return

    conn = duckdb.connect(db_path, read_only=True)
    
    print("="*60)
    print("      DATA ENGINEERING LAB - OBSERVABILITY HUB")
    print("="*60)
    
    print("\n[RECENT EXECUTION METRICS]")
    print(conn.execute("SELECT * FROM execution_metrics ORDER BY timestamp DESC LIMIT 5").df().to_string())
    
    print("\n[DATA DRIFT ALERTS (LAST 24H)]")
    print(conn.execute("SELECT * FROM drift_reports WHERE is_drifting = True ORDER BY timestamp DESC").df().to_string())
    
    print("="*60)

if __name__ == "__main__":
    main()
