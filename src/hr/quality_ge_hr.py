import great_expectations as ge
import pandas as pd

def validate_applicants(df):
    """
    Validates applicants against compliance rules:
    1. ISO Country allowed-list (USA, CAN, GBR, DEU, FRA).
    2. Email regex integrity.
    """
    if df.empty:
        return df, pd.DataFrame()

    # Convert to GE DataFrame
    ge_df = ge.from_pandas(df)

    # Rule 1: ISO Country Sovereignty (Allowed list)
    # We only accept applicants from these specific ISO-3 codes for this demo
    allowed_countries = ["USA", "CAN", "GBR", "DEU", "FRA", "SGP"]
    res_iso = ge_df.expect_column_values_to_be_in_set(
        "iso_country", 
        allowed_countries,
        result_format="COMPLETE"
    )

    # Rule 2: Email Pattern Integrity
    res_email = ge_df.expect_column_values_to_match_regex(
        "email",
        r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        result_format="COMPLETE"
    )

    # Identify valid vs invalid
    # A record is valid if it passes both sovereignty and regex checks
    iso_mask = ge_df["iso_country"].isin(allowed_countries)
    email_mask = ge_df["email"].str.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    
    valid_mask = iso_mask & email_mask
    
    valid_df = df[valid_mask].copy()
    quarantine_df = df[~valid_mask].copy()
    
    # Add failure reason to quarantine
    if not quarantine_df.empty:
        quarantine_df['failure_reason'] = "Compliance Breach (ISO/Regex)"
        
    print(f"Validation complete: {len(valid_df)} Passed, {len(quarantine_df)} Quarantined.")
    
    return valid_df, quarantine_df
