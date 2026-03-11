# Troubleshooting Operations

> [!NOTE]
> This document compiles frequent errors faced when operating the pipeline, outlining the specific **Root Cause** and **Enterprise Fix**.

---

## 1. Path Resolution: "ModuleNotFoundError: No module named 'src'"

> [!CAUTION]
> **Symptom**: Python interpreter fails to find `src.*` modules during testing.

**The Solution**:
Ensure you are running commands from the project root. We use `PYTHONPATH=/app` inside containers to guarantee that every script can locate the **src** and **tests** directories regardless of execution depth.

---

## 2. Authentication: "Invalid Credentials" in JupyterLab

> [!WARNING]
> **Symptom**: Token from `.env` is rejected by the Jupyter UI.

**The Fix**:
1. Execute: `docker exec -it pde_jupyter_lab jupyter server list`
2. Inspect the output. If the token is malformed, perform a hard reset:
   ```bash
   docker compose down -v
   docker compose up -d
   ```

---

## 3. Configuration: "`pytest.ini` unexpected line: '\ufeff[pytest]'"

> [!CAUTION]
> **Symptom**: Pytest chokes on a hidden Windows **UTF-8 BOM** signature.

**The Fix**:
Open the file in VS Code and change the encoding from `UTF-8 with BOM` back to **Pure UTF-8**. This ensures Unix-compatibility within the Docker environment.

---

## 4. Storage: "Used by another process" (Windows)

> [!TIP]
> **Symptom**: PowerShell blocks moving or deleting files inside the project.

**The Solution**:
1. Ensure no terminal is `.cd`'d into the target folder.
2. Shut down Docker containers/volumes.
3. Use **Resource Monitor (resmon)** to identify and terminate any processes holding file handles.
---

## 5. Streaming: "Kafka Connectivity Failure"

> [!CAUTION]
> **Symptom**: Producer or Spark job stalls with `Broker: No nodes available`.

**The Fix**:
1. Check Kafka health: `docker compose -f docker-compose.streaming.yml logs iot-kafka`.
2. Ensure the **KRaft Node ID** is 0 and the controller is bound to `iot-kafka:9093`.
3. If Kafka is unstable, perform a **Volume Cleanse**: `docker compose -f docker-compose.streaming.yml down -v && docker compose -f docker-compose.streaming.yml up -d`.

---

## 6. Spark: "Streaming Query Shutdown"

> [!WARNING]
> **Symptom**: Spark job dies immediately after starting.

**The Fix**:
1. Inspect the checkpoint directory: `/app/data/delta/_checkpoints`.
2. Delete old checkpoints if the schema has changed: `rm -rf data/delta/*/ _checkpoints`.
3. Verify that the **Spark Master URL** (`spark://iot-spark-master:7077`) is correctly exposed in `docker-compose.streaming.yml`.
---

## 7. Infrastructure: "failed to resolve image: not found"

> [!CAUTION]
> **Symptom**: Docker fails to pull `bitnami/*` images (e.g., Spark 3.5.1 or Kafka 3.7.0).

**The Root Cause**: 
Bitnami recently migrated non-latest tags of the free-tier catalog to a **Legacy Repository**. Standard `bitnami/` references for specific versions are being deprecated.

**The Fix**:
Update your `image:` tags in `docker-compose.streaming.yml` to use the legacy prefix:
- `bitnami/kafka:3.7.0` → **`bitnamilegacy/kafka:3.7.0`**
- `bitnami/spark:3.5.1` → **`bitnamilegacy/spark:3.5.1`**

---

## 8. Network: "Invalid master URL" (Spark Worker)

> [!IMPORTANT]
> **Symptom**: Spark worker fails to register with `SparkException: Invalid master URL`.

**The Root Cause**:
Java's `java.net.URI` class (used by Spark/Kafka) strictly follows **RFC 1123**. Hostnames **cannot** contain underscores (`_`). While Docker allows them in service names, the Java runtime rejects them as invalid characters.

**The Fix**:
Always use hyphens (`-`) for service and container names in the streaming stack:
- `iot_spark_master` (Illegal) → **`iot-spark-master`** (Compliant)

---

## 9. Environments: "PowerShell ParserError: TerminatorExpectedAtEndOfString"

> [!WARNING]
> **Symptom**: Orchestration scripts fail to run due to missing string terminators.

**The Root Cause**:
Windows PowerShell can struggle with **Character Encoding (UTF-8 with BOM)** when scripts contain complex emojis or special characters. This leads to misparsed string boundaries.

**The Fix**:
1. Save scripts as **Pure UTF-8** (No BOM).
2. Avoid using complex emojis in `Write-Host` or string constants within critical automation scripts.
---

## 10. Runtime: "Java gateway process exited before sending its port number"

> [!CAUTION]
> **Symptom**: PySpark applications crash immediately on startup inside a container.

**The Root Cause**:
The base Python image (e.g., `python:3.11-slim`) does not include the Java Runtime Environment (JRE). PySpark requires a JVM to communicate between the Python driver and the Spark executors.

**The Fix**:
Upgrade your **Dockerfile** to install a headless JRE and set the `JAVA_HOME` environment variable. 
```dockerfile
RUN apt-get update && apt-get install -y default-jre-headless
```

---

## 11. Metadata: "End of file expected" in `_delta_log/*.json`

> [!NOTE]
> **Symptom**: VS Code or IDEs show red syntax errors in Delta Lake transaction logs.

**The Root Cause**:
Delta Lake uses **JSONL (JSON Lines)** to maintain atomic transaction logs. Standard JSON validators expect a single root object, but Delta logs contain multiple objects (one per line).

**The Solution**:
**Ignore the warning.** This is the expected behavior for high-performance ACID logs. Spark and Delta Lake will parse the files correctly regardless of the IDE's validation errors.
