# scripts/payments/init_payments_db.py
from src.core.db import create_postgres_engine
from sqlalchemy import text
import sys
import os

def init_payments_db():
    try:
        engine = create_postgres_engine()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        sql_path = os.path.join(script_dir, 'init_payments_db.sql')
        
        with open(sql_path, 'r') as f:
            sql = f.read()
            
        with engine.connect() as conn:
            statements = [s.strip() for s in sql.split(';') if s.strip()]
            for statement in statements:
                conn.execute(text(statement))
            conn.commit()
            print("Payments Tables Created Successfully")
    except Exception as e:
        print(f"Error initializing Payments DB: {e}")
        sys.exit(1)

if __name__ == "__main__":
    init_payments_db()
