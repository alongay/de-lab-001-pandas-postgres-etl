import os
import psycopg2
from sqlalchemy import create_engine
import sys

def verify_bi_warehouse_connection():
    """
    Verifies that the Metabase instance can reach the PostgreSQL Warehouse.
    This simulates the 'ping' Metabase sends during DB setup.
    """
    db_name = os.getenv("POSTGRES_DB", "de_workshop")
    db_user = os.getenv("POSTGRES_USER", "de_user")
    db_pass = os.getenv("POSTGRES_PASSWORD", "de_password")
    db_host = "postgres"  # Internal Docker alias
    db_port = "5432"

    print(f"🔍 Testing BI Connectivity to {db_host}:{db_port}/{db_name}...")
    
    try:
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_pass,
            host=db_host,
            port=db_port,
            connect_timeout=5
        )
        print("✅ SUCCESS: Warehouse is reachable from the BI network.")
        
        # Check for core tables
        cur = conn.cursor()
        cur.execute("SELECT table_schema, table_name FROM information_schema.tables WHERE table_schema IN ('payments', 'hr');")
        tables = cur.fetchall()
        print(f"📊 Found {len(tables)} Production-ready tables for BI consumption.")
        
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ FAILURE: Could not connect to Warehouse. Error: {e}")
        return False

if __name__ == "__main__":
    if not verify_bi_warehouse_connection():
        sys.exit(1)
