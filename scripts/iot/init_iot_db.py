from src.core.db import create_postgres_engine
from sqlalchemy import text
import sys

def init_iot_db():
    try:
        engine = create_postgres_engine()
        import os
        script_dir = os.path.dirname(os.path.abspath(__file__))
        sql_path = os.path.join(script_dir, 'init_iot_db.sql')
        with open(sql_path, 'r') as f:
            sql = f.read()
            
        with engine.connect() as conn:
            # SQLAlchemy text() execute doesn't always support multiple statements in one call
            # with certain drivers. We'll split by semicolon for safety.
            statements = [s.strip() for s in sql.split(';') if s.strip()]
            for statement in statements:
                conn.execute(text(statement))
            conn.commit()
            print("IoT Tables Created Successfully")
    except Exception as e:
        print(f"Error initializing IoT DB: {e}")
        sys.exit(1)

if __name__ == "__main__":
    init_iot_db()
