import pandas as pd
import logging
import re

# Configure logging to hide PII
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/etl.log"),
        logging.StreamHandler()
    ]
)

def redact_pii(text):
    """
    Helper to redact potential PII for logging.
    """
    if not isinstance(text, str):
        return text
    # Simple regex for email/phone patterns
    email_regex = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    return re.sub(email_regex, "[REDACTED]", text)

def transform_applicants(df):
    """
    Transforms applicant data, implementing PII redaction for logs.
    """
    logging.info("Starting HR Transformation...")
    
    # Log redacted sample for auditing without leaking PII
    sample_email = df['email'].iloc[0] if not df.empty else "N/A"
    logging.info(f"Processing applicant data. Sample email: {redact_pii(sample_email)}")

    # Standardize columns
    df['email'] = df['email'].str.strip().str.lower()
    df['full_name'] = df['full_name'].str.strip().str.title()
    df['iso_country'] = df['iso_country'].str.strip().str.upper()
    
    # Add extraction timestamp
    df['ingested_at'] = pd.Timestamp.utcnow()
    
    return df
