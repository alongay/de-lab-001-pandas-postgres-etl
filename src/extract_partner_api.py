import os
import json
from typing import Any, Dict, List
from urllib.parse import urlparse

import pandas as pd
import requests

def extract_partner_api() -> pd.DataFrame:
    """
    Extracts JSON payment payload from Partner A via API_URL or a local JSON mock.
    Returns a DataFrame with the raw camelCase schema + partner_id injected.
    """
    api_url = os.getenv("API_URL", "").strip()
    partner_id = os.getenv("PARTNER_API_ID", "partner_api")

    # Local Mock Handle
    if api_url.startswith("file://") or api_url == "https://example.partner/api/orders":
        json_path = os.getenv("JSON_PATH", "data/inbound/transactions.json")
        with open(json_path, "r", encoding="utf-8-sig") as f:
            payload = json.load(f)
    else:
        parsed = urlparse(api_url)
        if parsed.scheme.lower() != "https" or not parsed.netloc:
            raise ValueError(f"API_URL must be a valid HTTPS URI. Got: {api_url}")
            
        session = requests.Session()
        headers = {"Accept": "application/json", "User-Agent": "de-lab/1.0"}
        response = session.get(api_url, headers=headers, timeout=30)
        response.raise_for_status()
        payload = response.json()

    if not isinstance(payload, list):
        raise TypeError(f"Expected JSON array (list). Got: {type(payload).__name__}")

    rows: List[Dict[str, Any]] = []
    for idx, item in enumerate(payload):
        if not isinstance(item, dict):
            raise TypeError(f"Item {idx} is {type(item).__name__}, expected dict.")
        item["_partner_marker"] = partner_id  # Inject to help mapping downstream
        rows.append(item)

    return pd.DataFrame(rows)
