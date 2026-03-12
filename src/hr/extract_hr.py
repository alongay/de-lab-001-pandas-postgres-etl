import os
import pandas as pd

def extract_applicants():
    """
    Extracts HR applicant data from the inbound data directory.
    """
    inbound_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/hr/inbound"))
    
    if not os.path.exists(inbound_dir):
        return None

    csv_files = [os.path.join(inbound_dir, f) for f in os.listdir(inbound_dir) if f.endswith('.csv')]
    if not csv_files:
        return None

    # Load all CSVs and combine
    dfs = [pd.read_csv(f) for f in csv_files]
    return pd.concat(dfs, ignore_index=True)
