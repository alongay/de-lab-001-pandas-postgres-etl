import great_expectations as ge
import pandas as pd
from typing import Dict, Any

def validate_iot_telemetry(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Refined Quality Gate: Encodes "Laws of Physics" + Integrity.
    
    1. Physical Bounds:
       - temp_c: -40 to 85
       - humidity_pct: 0 to 100
       - pressure_hpa: 300 to 1100
    2. Time-Series Integrity:
       - (partner_id, device_id, reading_ts, metric) uniqueness.
    3. Unit Consistency:
       - Metric-specific unit enforcement.
    """
    if df.empty:
        return {"success": True, "statistics": {"evaluated_expectations": 0}}
        
    gdf = ge.from_pandas(df)
    
    # 1. Identity & Context (Null Checks)
    for col in ["partner_id", "device_id", "metric", "reading_ts"]:
        gdf.expect_column_values_to_not_be_null(col)
    
    # 2. Physics Bounds Checking
    # temp_c: -40C to 85C
    gdf.expect_column_values_to_be_between(
        "value", min_value=-40.0, max_value=85.0,
        condition_parser="pandas", row_condition='metric == "temp_c"'
    )
    # humidity_pct: 0% to 100%
    gdf.expect_column_values_to_be_between(
        "value", min_value=0.0, max_value=100.0,
        condition_parser="pandas", row_condition='metric == "humidity_pct"'
    )
    # pressure_hpa: 300hPa to 1100hPa
    gdf.expect_column_values_to_be_between(
        "value", min_value=300.0, max_value=1100.0,
        condition_parser="pandas", row_condition='metric == "pressure_hpa"'
    )
    
    # 3. Unit Consistency (Strict Mapping)
    gdf.expect_column_values_to_be_in_set("unit", ["c"], condition_parser="pandas", row_condition='metric == "temp_c"')
    gdf.expect_column_values_to_be_in_set("unit", ["pct"], condition_parser="pandas", row_condition='metric == "humidity_pct"')
    gdf.expect_column_values_to_be_in_set("unit", ["hpa"], condition_parser="pandas", row_condition='metric == "pressure_hpa"')

    # 4. Integrity Check (Compound Uniqueness)
    gdf.expect_compound_columns_to_be_unique(["partner_id", "device_id", "reading_ts", "metric"])

    results = gdf.validate()
    return results.to_json_dict()
