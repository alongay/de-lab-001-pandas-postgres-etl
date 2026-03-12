import os
import sys
import pandas as pd
from datetime import datetime

# Symmetrical Pathing
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from hr.extract_hr import extract_applicants
from hr.transform_hr import transform_applicants
from hr.quality_ge_hr import validate_applicants
from hr.load_hr import load_applicants

def run_hr_etl():
    print(f"\n--- Starting HR Applicant Intake (PII Compliance) at {datetime.now()} ---")
    
    # 1. Extract
    raw_df = extract_applicants()
    if raw_df is None or raw_df.empty:
        print("No new applicants found.")
        return

    # 2. Transform (PII Redaction + Cleaning)
    clean_df = transform_applicants(raw_df)

    # 3. Quality (Sovereignty + Identity Integrity)
    valid_df, quarantine_df = validate_applicants(clean_df)

    # 4. Load
    load_applicants(valid_df, quarantine_df)
    
    print("--- HR ETL Complete ---\n")

if __name__ == "__main__":
    run_hr_etl()
