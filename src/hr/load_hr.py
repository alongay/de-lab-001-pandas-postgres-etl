import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

def load_applicants(valid_df, quarantine_df):
    """
    Persists HR applicant data to Postgres.
    """
    db_url = os.getenv("DB_URL", "postgresql://pde_user:pde_password@localhost:5432/pde_db")
    engine = create_engine(db_url)

    if not valid_df.empty:
        valid_df.to_sql(
            "hr_applicants", 
            engine, 
            if_exists="append", 
            index=False,
            schema="public"
        )
        print(f"Loaded {len(valid_df)} records to hr_applicants.")

    if not quarantine_df.empty:
        quarantine_df.to_sql(
            "hr_applicants_quarantine", 
            engine, 
            if_exists="append", 
            index=False,
            schema="public"
        )
        print(f"Quarantined {len(quarantine_df)} records to hr_applicants_quarantine.")
