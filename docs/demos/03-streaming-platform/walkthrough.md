# Walkthrough: Demo 3 — Streaming Event Platform

This script guides you through a high-impact presentation of **Real-Time Data Engineering**.

## 1. The Environment Setup
**Action**: Start the streaming infrastructure.
**Command**: `.\task.ps1 up` (Starts core lab)
**Talk Track**: 
- "We are initializing an enterprise-grade cluster locally. We have **Postgres** for our warehouse, **Kafka** for our event bus, and a **Spark Master/Worker** cluster for our real-time compute."

---

## 2. Launching the Platform
**Action**: Run the integrated streaming demo.
**Command**: `.\task.ps1 demo-iot-stream`

**What is happening?**
1. **Infrastructure**: Containers start.
2. **Broker**: Kafka creates the `iot.telemetry.raw` topic.
3. **Compute**: Spark starts a Structured Streaming query.
4. **Ingestion**: The IoT Producer begins firing events.

---

## 3. Real-Time Logic (The "Magic")
**Action**: Observe the terminal output.
**Talk Track**:
- "Notice the Spark logs. Every 2 seconds, Spark processes a micro-batch of hundreds of events."
- "We are using a **Medallion Architecture**. Raw events land in the **Bronze Delta Table** instantly."
- "Simultaneously, our **Spark Quality Gate** evaluates every record. If a sensor reports a temperature of 999.9 (chaos), it is filtered into the **Quarantine Table**, while valid data moves to **Silver**."

### 🔬 Multi-Sink Observability
**Action**: Verify the Medallion Split in real-time.
**Command**: 
```powershell
# 1. Check for Silver/Quarantine processing in logs
docker compose -f docker-compose.streaming.yml logs iot-silver-stream --tail 50

# 2. Count refined data files
Get-ChildItem data/iot/delta/silver/_delta_log | select -last 5
Get-ChildItem data/iot/delta/quarantine/_delta_log | select -last 5
```

---

## 4. Verifying the Delta Lake
**Action**: List the Delta Lake directory.
**Command**: `ls -R data/iot/delta/`
**Talk Track**:
- "Unlike a simple CSV, these are **Delta Tables**. We have transaction logs and parquet files that support **ACID transactions** and **Time Travel**."

---

## 5. Senior-Level Verification
**Action**: Check for anomalies.
**Command**: (Runs automatically at the end of `demo-iot-stream`)
**Result**: `Anomalies Detected!`
**Talk Track**:
- "Our pipeline isn't just fast; it's **Self-Healing**. We detected the injected chaos and moved it to quarantine without stopping the entire stream."

---

## 6. Cleanup & Reset
**Action**: Reset the environment for the next run.
**Command**: `.\scripts\streaming\reset_delta_lake.ps1`
**Talk Track**:
- "To maintain a clean lab, we have an automated script that wipes the Delta Lake and clears the Spark checkpoints. This ensures that every time we present, we are starting from a true 'Empty State'."

---

> [!TIP]
> **Pro Tip**: Open the [**Real-Time Profiling Notebook**](../../../notebooks/streaming/04_iot_streaming_audit.ipynb) *during* the stream to show the data counts climbing and the 'Time Travel' versions accumulating in the transaction log.
