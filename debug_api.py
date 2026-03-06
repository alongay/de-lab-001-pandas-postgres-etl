import os
import traceback
from src.extract import extract_partner_data
from src.transform import transform_orders_dataframe

try:
    os.environ["API_URL"] = "file:///app/data/inbound/partner_orders.json"
    os.environ["INGEST_SOURCE"] = "api"

    df = extract_partner_data()
    print("COLS:", list(df.columns))
    
    tr = transform_orders_dataframe(df)
    print("SUCCESS!")
    print(tr.dataframe.head())
except Exception as e:
    print("ERROR!")
    traceback.print_exc()
