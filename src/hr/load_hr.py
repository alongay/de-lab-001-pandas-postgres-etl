from src.core.db import create_postgres_engine

def load_applicants(valid_df, quarantine_df):
    """
    Persists HR applicant data to Postgres.
    """
    engine = create_postgres_engine()

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
