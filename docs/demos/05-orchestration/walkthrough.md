# Walkthrough: Demo 5 — Enterprise Data Platform Orchestration

![Airflow DAG Status](file:///C:/Users/along/.gemini/antigravity/brain/c94d33df-1d63-4e97-a5a4-fb63ccf7673b/airflow_dag_list_1773287125043.png)

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

### 🛠️ Demo: The Chaos Run
This section proves the platform's **Governance** by simulating an SLA breach in the streaming layer.

1.  **Inject Chaos**: Manually stop the streaming consumer: `docker stop pde-iot-silver-stream`.
2.  **Observe Monitoring**: The `iot_stream_health_monitor` DAG in Airflow will fire on its next schedule (every 5 mins).
3.  **Detect SLA Breach**: The DAG will detect that the `Silver` Delta table has not advanced in the last 5 minutes.
4.  **Automatic Alerting**: Check the Airflow logs for the `notify_sla_breach` task. It will log a mock alert to the "Critical Operations" channel.
5.  **Recovery**: Restart the container (`docker start pde-iot-silver-stream`) and watch the DAG return to a `Success` state once data flow resumes.

> [!CAUTION]
> **Interview Point**: "This is **Proactive Orchestration**. Instead of waiting for a user to complain that a dashboard is stale, I implemented an Airflow-based health monitor that audits the Delta transaction logs in real-time. If the 'Freshness' SLA is breached, the platform automatically alerts operations before the business is impacted."

---

## 🎨 Operational Patterns (Interview Signal)
- **Pattern**: "I don't just run code; I verify the **Metadata** (GE JSONs) and **Delta Logs** to ensure the platform's physical integrity."
- **Isolation**: "My orchestration layer lives on a separate, bridge-isolated network for secure service discovery."
- **Resilience**: "I use Airflow as a monitor for streaming, not just a scheduler, to minimize restart overhead."
