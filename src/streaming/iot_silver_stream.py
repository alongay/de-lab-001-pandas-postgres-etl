"""
src/streaming/iot_silver_stream.py

Medallion Architecture: Silver Layer
Goal: Read from Bronze, apply Quality Gates, and split into Silver and Quarantine sinks.
"""

from pyspark.sql import SparkSession
from src.streaming.iot_rules import (
    BRONZE_PATH,
    SILVER_PATH,
    QUARANTINE_PATH,
    CHECKPOINT_SILVER
)
from src.streaming.iot_quality_spark import process_micro_batch

def run_silver_stream():
    spark = SparkSession.builder \
        .appName("IoT-Silver-Stream") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,io.delta:delta-spark_2.12:3.2.0") \
        .getOrCreate()

    print(f"🌊 Silver: Consuming from Bronze at {BRONZE_PATH}...")

    # 1. Read from Bronze (Delta)
    bronze_stream = spark.readStream \
        .format("delta") \
        .load(BRONZE_PATH)

    # 2. Wrap the processing logic in a Multi-Sink foreachBatch
    def write_to_sinks(batch_df, batch_id):
        # Apply standardizations and flags
        processed_batch = process_micro_batch(batch_df, batch_id)
        
        # Split into Valid and Anomaly
        valid_df = processed_batch.filter("is_anomaly == false").drop("is_anomaly", "anomaly_reason")
        anomaly_df = processed_batch.filter("is_anomaly == true")
        
        v_count = valid_df.count()
        a_count = anomaly_df.count()
        print(f"✅ Batch {batch_id}: Processed {v_count + a_count} rows. (Silver: {v_count}, Quarantine: {a_count})", flush=True)

        # Write to Silver (Clean)
        if v_count > 0:
            valid_df.write.format("delta").mode("append").save(SILVER_PATH)
            
        # Write to Quarantine (Anomalies)
        if a_count > 0:
            anomaly_df.write.format("delta").mode("append").save(QUARANTINE_PATH)

    # 3. Start the stream with foreachBatch
    query = bronze_stream.writeStream \
        .foreachBatch(write_to_sinks) \
        .option("checkpointLocation", CHECKPOINT_SILVER) \
        .start()

    print(f"🚀 Silver stream active. Clean data -> {SILVER_PATH}, Anomalies -> {QUARANTINE_PATH}")
    query.awaitTermination()

if __name__ == "__main__":
    run_silver_stream()
