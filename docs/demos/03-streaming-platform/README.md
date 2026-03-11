# Demo 3: Streaming Event Platform (Real-Time IoT)

**Status: ✅ Operational / Enterprise Ready**

### 🎯 The Pitch
This demo upgrades the lab from **Batch IoT** to **Real-Time Streaming**. We transition from periodic file drops to a high-velocity event-driven architecture using **Kafka** and **Spark Structured Streaming**. This is the definitive "Senior Data Engineer" demo, showcasing stateful processing and the **Medallion Architecture** (Bronze/Silver).

### 🏗️ Architecture
- **Producer**: Python script emulating multiple IoT devices pushing JSON events to Kafka at 1k+ events/sec.
- **Messaging**: **Kafka (KRaft Mode)** for high-throughput distributed messaging.
- **Compute**: **Spark Structured Streaming** (Master/Worker) for micro-batch processing.
- **Storage**: **Delta Lake** on the local filesystem (Open-source ACID storage).
- **Quality**: **Inline Spark Quality Gate** that flags anomalies in real-time before landing in the Silver layer.

### 🛠️ Technical Challenges & "War Stories"
- **Java Runtime Isolation**: Navigating the transition from local Spark to a containerized PySpark driver, which required injecting an **OpenJDK 17 JRE** into the base Python image.
- **Hostname Protocol**: Solving the Spark-to-Master connectivity by standardizing on **RFC 1123 compliant hyphens** (e.g., `iot-kafka`) to satisfy Java's strict URI requirements.
- **Micro-Batch Observability**: Implementing a custom `foreachBatch` logic with inline row-counts to provide a "Proof of Life" during real-time ingestion.
- **Dependency Loading**: Automating the injection of `spark-sql-kafka` and `delta-spark` Maven jars directly through the `SparkSession` builder to eliminate manual jar management.

### 🎓 Teaching Flow
1. **Infrastructure Spin-up**: Deploy Kafka, Spark, and Postgres in one cluster.
2. **Stream Initialization**: Start the Spark job and observe it awaiting events.
3. **Live Ingestion**: Fire up the IoT Producer and watch the terminal logs "come alive."
4. **Delta Time-Travel**: Use the [**Streaming Profiling Notebook**](../../../notebooks/streaming/04_iot_streaming_audit.ipynb) to query live results and transaction history.
5. **Clean State**: Use the [**Reset Delta Lake Script**](../../../scripts/streaming/reset_delta_lake.ps1) to wipe the environment between presentations.
6. **Physical Chaos**: Observe the **Spark Quality Gate** automatically splitting outliers into a dedicated **Quarantine Delta Table** in real-time.

---

> [!TIP]
> **Interview "Gold"**: Explain how you used Spark's `writeStream` with `.format("delta")` to provide ACID guarantees to a streaming pipeline that would traditionally be prone to data corruption during crashes.
