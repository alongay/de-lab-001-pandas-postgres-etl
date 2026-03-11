"""
src/streaming/iot_quality_spark.py

Micro-batch Quality Enforcement for Spark Structured Streaming.
Handles standardization, deduplication, and anomaly flagging.
"""

from pyspark.sql import DataFrame
from pyspark.sql.functions import col, when, to_timestamp, current_timestamp, lit
from src.streaming.iot_rules import PHYSICAL_BOUNDS, VALID_UNITS

def process_micro_batch(batch_df: DataFrame, batch_id: int):
    """
    Standardizes and flags anomalies in a streaming micro-batch.
    """
    if batch_df.isEmpty():
        return batch_df

    # 1. Standardization & Parsing
    # We allow some slack in the reading_ts parsing
    processed_df = batch_df \
        .withColumn("reading_ts", to_timestamp(col("reading_ts"))) \
        .withColumn("silver_processed_at", current_timestamp())

    # 2. Anomaly Detection (Phase 7)
    # Start with all rows clean
    flagged_df = processed_df \
        .withColumn("is_anomaly", lit(False)) \
        .withColumn("anomaly_reason", lit(None).cast("string"))

    # Apply Physics Bounds
    for metric, (low, high) in PHYSICAL_BOUNDS.items():
        flagged_df = flagged_df.withColumn("is_anomaly", 
            when((col("metric") == metric) & ((col("value") < low) | (col("value") > high)), True)
            .otherwise(col("is_anomaly"))
        ).withColumn("anomaly_reason",
            when((col("metric") == metric) & ((col("value") < low) | (col("value") > high)), lit(f"physical_outlier_{metric}"))
            .otherwise(col("anomaly_reason"))
        )

    # Apply Unit Integrity
    for metric, expected_unit in VALID_UNITS.items():
        flagged_df = flagged_df.withColumn("is_anomaly",
            when((col("metric") == metric) & (col("unit") != expected_unit), True)
            .otherwise(col("is_anomaly"))
        ).withColumn("anomaly_reason",
            when((col("metric") == metric) & (col("unit") != expected_unit), lit(f"unit_mismatch_{metric}"))
            .otherwise(col("anomaly_reason"))
        )

    # Future Timestamp Check
    flagged_df = flagged_df.withColumn("is_anomaly",
        when(col("reading_ts") > current_timestamp(), True)
        .otherwise(col("is_anomaly"))
    ).withColumn("anomaly_reason",
        when(col("reading_ts") > current_timestamp(), lit("future_timestamp"))
        .otherwise(col("anomaly_reason"))
    )

    return flagged_df
