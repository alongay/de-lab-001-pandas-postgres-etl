# Demo 4 Walkthrough: Enterprise Data Platform Orchestration

This demo showcases how to orchestrate batch and streaming pipelines at scale using **Apache Airflow**.

## 🏗️ Architecture & Features

### 1. Slim-Production Orchestration
- **Webserver & Scheduler**: Running on port **8088** to avoid conflicts with Spark (8080).
- **LocalExecutor**: Optimized for local performance while maintaining parallel task execution.
- **Shared Network**: All services (Postgres, Kafka, Spark) are joined to `pde_platform_net` for intentional service discovery.

### 3. Symmetrized Isolation (Enterprise Standards)
- **Source Code**: Centralized logic in `src/orchestration/platform_utils.py` for SLA and Audit checks.
- **Management Scripts**: Modular PSU/Python scripts in `scripts/orchestration/` for platform lifecycle.
- **Analytical Audit**: Dedicated `notebooks/orchestration/` for platform metadata exploration.

---

## ✅ Verification & Proof of Work

### 1) Initialize & Start Platform
Use the standardized task runner commands:
```powershell
.\task.ps1 demo-orchestration
```
*This command executes idempotent initialization via `scripts/orchestration/platform_init.ps1`.*

### 2) Verify DAG & Source Integrity
Check that all DAGs are correctly registered and importing from the `src/` package:
```powershell
.\task.ps1 platform-status
```
*Validated via the CI-ready `dag_validator.py` script.*

### 3) Access Monitoring UI
- **Airflow**: [http://localhost:8088](http://localhost:8088) (`admin`/`admin`)
- **Spark Master**: [http://localhost:8080](http://localhost:8080)
- **Spark Worker**: [http://localhost:8081](http://localhost:8081)

### 4) Trigger a Quality Breach (SLA Failure)
1. Stop the `iot-silver-stream` container: `docker stop pde-iot-silver-stream`.
2. Wait 5 minutes.
3. Observe the `iot_stream_health_monitor` DAG in Airflow.
4. Check the scheduler logs for the **Mock alert box** triggered by the SLA Breach.

---

## 🎨 Operational Patterns (Interview Signal)
- **Pattern**: "I don't just run code; I verify the **Metadata** (GE JSONs) and **Delta Logs** to ensure the platform's physical integrity."
- **Isolation**: "My orchestration layer lives on a separate, bridge-isolated network for secure service discovery."
- **Resilience**: "I use Airflow as a monitor for streaming, not just a scheduler, to minimize restart overhead."
