import os
import pandas as pd
import pytest
from unittest.mock import patch, mock_open

from src.payments.extract_partner_csv import extract_partner_csv
from src.payments.extract_partner_api import extract_partner_api


@patch.dict(os.environ, {"CSV_PATH": "/fake/path.csv", "PARTNER_CSV_ID": "partner_csv"})
@patch("os.path.exists", return_value=True)
@patch("pandas.read_csv")
def test_extract_csv(mock_read_csv, mock_exists):
    mock_df = pd.DataFrame([{"order_id": "1"}])
    mock_read_csv.return_value = mock_df

    df = extract_partner_csv()
    assert df.shape[0] == 1
    assert df.iloc[0]["_partner_marker"] == "partner_csv"
    mock_read_csv.assert_called_once_with("/fake/path.csv")


@patch.dict(os.environ, {"API_URL": "file:///fake/orders.json", "PARTNER_API_ID": "partner_api"})
@patch("builtins.open", new_callable=mock_open, read_data='[{"orderId": "1"}]')
def test_extract_api_local_file(mock_file):
    df = extract_partner_api()
    assert df.shape[0] == 1
    assert df.iloc[0]["_partner_marker"] == "partner_api"


@patch.dict(os.environ, {"API_URL": "https://api.example.com/orders", "PARTNER_API_ID": "partner_api"})
@patch("requests.Session.get")
def test_extract_api_https(mock_get):
    class MockResponse:
        def raise_for_status(self): pass
        def json(self): return [{"orderId": "1"}]
        
    mock_get.return_value = MockResponse()

    df = extract_partner_api()
    assert df.shape[0] == 1
    assert df.iloc[0]["_partner_marker"] == "partner_api"
