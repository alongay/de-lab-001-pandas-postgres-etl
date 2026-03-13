"""
src/streaming/iot_bronze_stream.py

Medallion Architecture: Bronze Layer
Goal: Read from Kafka and land raw truth into Delta Lake with minimal overhead.
"""

import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, current_timestamp
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType

from src.streaming.iot_rules import (
    IOT_RAW_TOPIC,
    BRONZE_PATH,
    CHECKPOINT_BRONZE
)

def run_bronze_stream():
    KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "iot-kafka:9092")
    
    spark = SparkSession.builder \
        .appName("IoT-Bronze-Stream") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,io.delta:delta-spark_2.12:3.2.0") \
        .getOrCreate()

    # 1. Define Raw Schema (for parsing JSON stream)
    schema = StructType([
        StructField("device_id", StringType(), True),
        StructField("reading_ts", StringType(), True), # Raw string for parsing at Silver
        StructField("metric", StringType(), True),
        StructField("value", DoubleType(), True),
        StructField("unit", StringType(), True),
        StructField("partner_id", StringType(), True),
        StructField("event_id", StringType(), True),
        StructField("ingested_at", StringType(), True)
    ])

    print(f"📡 Bronze: Consuming from topic '{IOT_RAW_TOPIC}'...")

    # 2. Read from Kafka
    raw_stream = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP) \
        .option("subscribe", IOT_RAW_TOPIC) \
        .option("startingOffsets", "latest") \
        .load()

    # 3. Parse JSON and add Ingestion Metadata
    bronze_df = raw_stream.selectExpr("CAST(value AS STRING) as json_payload") \
        .select(from_json(col("json_payload"), schema).alias("data")) \
        .select("data.*") \
        .withColumn("bronze_ingested_at", current_timestamp())

    # 4. Write to Delta Bronze (Append Only)
    query = bronze_df.writeStream \
        .format("delta") \
        .outputMode("append") \
        .option("checkpointLocation", CHECKPOINT_BRONZE) \
        .start(BRONZE_PATH)

    print(f"🚀 Bronze stream active. Data landing at: {BRONZE_PATH}")
    query.awaitTermination()

if __name__ == "__main__":
    run_bronze_stream()
