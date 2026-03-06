import os
import pandas as pd

def extract_partner_csv() -> pd.DataFrame:
    """
    Extracts CSV payment payload from Partner B via a localized drop file.
    Returns a DataFrame with the raw snake_case schema + partner_id injected.
    """
    csv_path = os.getenv("CSV_PATH", "data/inbound/transactions_daily.csv")
    partner_id = os.getenv("PARTNER_CSV_ID", "partner_csv")
    
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Missing CSV at {csv_path}")
        
    df = pd.read_csv(csv_path)
    
    if df.empty:
        return df
        
    df["_partner_marker"] = partner_id
    
    return df
