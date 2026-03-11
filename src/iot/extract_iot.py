import os
import json
import requests
import pandas as pd
from typing import Any, Dict, List
from urllib.parse import urlparse

def read_iot_json_from_api_url(iot_api_url: str) -> List[Dict[str, Any]]:
    """
    Reads IoT JSON from a file:// mock or a real https endpoint.
    """
    if not iot_api_url:
        return []

    # Local Mock or File Handle
    if iot_api_url.startswith("file://") or "telemetry.json" in iot_api_url:
        json_path = iot_api_url.replace("file://", "")
        # Handle relative/absolute container paths
        if not os.path.isabs(json_path) and not json_path.startswith("/app"):
             json_path = os.path.join("data", "iot", "inbound", "telemetry.json")
        
        # Map /app prefix to local if running outside container
        if json_path.startswith("/app"):
            json_path = json_path.replace("/app", ".")

        if not os.path.exists(json_path):
             raise FileNotFoundError(f"Missing IoT JSON mock at {json_path}")

        with open(json_path, "r", encoding="utf-8-sig") as f:
            return json.load(f)
    else:
        # Production HTTPS endpoint
        parsed = urlparse(iot_api_url)
        if parsed.scheme.lower() != "https" or not parsed.netloc:
            raise ValueError(f"IoT API_URL must be HTTPS. Got: {iot_api_url}")
            
        session = requests.Session()
        headers = {"Accept": "application/json", "User-Agent": "de-lab-iot/1.0"}
        response = session.get(iot_api_url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()

def read_iot_csv(iot_csv_path: str) -> pd.DataFrame:
    """
    Reads the IoT CSV telemetry file.
    """
    if not os.path.exists(iot_csv_path):
        raise FileNotFoundError(f"Missing IoT CSV at {iot_csv_path}")
    return pd.read_csv(iot_csv_path)

def extract_iot(ingest_source: str = None) -> pd.DataFrame:
    """
    Extracts sensor telemetry based on IOT_INGEST_SOURCE env var.
    Returns a DataFrame with raw columns.
    """
    if ingest_source is None:
        ingest_source = os.getenv("IOT_INGEST_SOURCE", "both").lower()
    
    dfs = []
    
    # 1. API Source (JSON)
    if ingest_source in ["api", "both"]:
        url = os.getenv("IOT_API_URL", "data/iot/inbound/telemetry.json")
        partner_id = os.getenv("IOT_PARTNER_API_ID", "iot_api")
        data = read_iot_json_from_api_url(url)
        df_api = pd.DataFrame(data)
        df_api["_partner_marker"] = partner_id
        dfs.append(df_api)
        
    # 2. CSV Source (Batch)
    if ingest_source in ["csv", "both"]:
        path = os.getenv("IOT_CSV_PATH", "data/iot/inbound/telemetry.csv")
        partner_id = os.getenv("IOT_PARTNER_CSV_ID", "iot_csv")
        df_csv = read_iot_csv(path)
        df_csv["_partner_marker"] = partner_id
        dfs.append(df_csv)
        
    if not dfs:
        return pd.DataFrame()
        
    return pd.concat(dfs, ignore_index=True)
