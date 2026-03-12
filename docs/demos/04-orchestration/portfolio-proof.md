# Portfolio Proof: Demo 4 (Orchestration & Governance)

## 🏢 Enterprise Architecture
Demo 4 integrates all previous building blocks into a supervised platform. Batch ETL is managed by **Apache Airflow**, while streaming health is monitored via automated SLA checks against **Delta Lake** commit activity.

![Airflow DAG List](file:///C:/Users/along/.gemini/antigravity/brain/c94d33df-1d63-4e97-a5a4-fb63ccf7673b/airflow_dag_list_1773281136221.png)
*Figure 1: Airflow UI showing the production-ready pipelines for Payments, IoT, and Streaming Monitor.*

## 🚀 Key Proof Points

### 1. Supervised Orchestration
The **Payments ETL Pipeline** is designed with a "Wait-Transform-Verify" pattern. It ensures data existence via sensors before executing logic, preventing ghost runs.

![Payments ETL Graph](file:///C:/Users/along/.gemini/antigravity/brain/c94d33df-1d63-4e97-a5a4-fb63ccf7673b/airflow_payments_graph_view_1773281198436.png)
*Figure 2: payments_etl_pipeline graph view illustrating the dependency flow and quality gate integration.*

### 2. Compute Isolation (Spark)
All heavy compute is offloaded to a dedicated Spark cluster, visible in the Master UI. This separates the "Brain" (Airflow) from the "Brawn" (Spark).

![Spark Master UI](file:///C:/Users/along/.gemini/antigravity/brain/c94d33df-1d63-4e97-a5a4-fb63ccf7673b/spark_master_ui_1773281211075.png)
*Figure 3: Spark Master UI confirming the compute cluster is active and serving the streaming workers.*

### 3. Delta Lake Persistence (Medallion Proof)
The streaming demo continuously writes to Delta Lake. Below is a snapshot of the `_delta_log` directory for the **Silver** table, showing 300+ atomic commits—proof of a high-velocity production environment.

```bash
# Directory: data/streaming/delta/silver/_delta_log
00000000000000000320.json
00000000000000000321.json
00000000000000000322.json
00000000000000000323.json
_last_checkpoint
```

### 4. SLA & Quality Alerting
We tested the platform's response to a **forced failure** (negative transaction amount). The system correctly identified the breach and fired an alert to our mock notification system.

**Terminal Evidence:**
```text
########################################
PIPELINE: payments_etl_pipeline
TASK:     run_payments_etl
MESSAGE:  Failing with: Great Expectations validation failed for column 'amount'...
########################################
```

## 🛠️ Infrastructure Commands
To replicate this environment:
```powershell
# Initialize platform
.\task.ps1 platform-init
# Spin up hybrid batch/streaming platform
.\task.ps1 demo-orchestration
# Check health
.\task.ps1 platform-status
```

## 🧠 Interview Talk Tracks
- **Orchestration vs. Execution**: "I use Airflow as the control plane, but Spark/Docker handle the execution. This ensures the scheduler isn't bogged down by data loads."
- **Data Freshness**: "Demo 4 implements a dedicated monitor that scans Delta Lake `_delta_log` files for staleness—if no commit arrives within 5 minutes, it triggers an SLA alert."
