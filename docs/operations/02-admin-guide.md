# System Administration Guide (Admin SOP)

This document serves as the **Standard Operating Procedure (SOP)** for the administration, maintenance, and lifecycle management of the Data Engineering Lab. While the [Runbook](../operations/01-sop-runbook.md) focuses on daily data tasks, this guide focuses on **Platform Reliability**.

---

## 🏗️ 1. Platform Governance Matrix

| Task Area | Frequency | Tooling | Responsibility |
| :--- | :--- | :--- | :--- |
| **Network Integrity** | After Restart | `.\task.ps1 platform-status` | Ensure `pde_platform_net` isolation. |
| **Schema Evolution** | On Migration | `docker exec pde-airflow-scheduler airflow dags reserialize` | Sync DAGs with new physical models. |
| **Log Rotation** | Monthly | `docker compose -f ... down -v` | Clear transient data lake partitions. |
| **Secret Audit** | Continuous | `.gitignore` + `scan_secrets.sh` | Prevent `.env` leakage to GitHub. |

---

## 🛠️ 2. Core Administrative Procedures

### A. Lifecycle Management (Orchestration)
The orchestration layer (Airflow) requires specific initialization to handle the **Symmetrical Modular Monolith** pattern.

1. **Initialization**: `.\task.ps1 platform-init` (Idempotent; safe to run anytime).
2. **Rebuild**: If adding new Python dependencies to DAGs:
   ```powershell
   docker compose -f docker-compose.orchestration.yml build --no-cache
   .\task.ps1 platform-up
   ```
3. **DAG Reserialization**: If Airflow UI shows stale code despite file changes:
   ```powershell
   docker exec pde-airflow-scheduler airflow dags reserialize
   ```

### B. Storage & Partitioning Administration
Our IoT and Streaming domains use **Delta Lake** and **Postgres Partitioning**.

- **Postgres Bloat Check**: If performance drops on Demo 2 (IoT), check the partition count:
  ```sql
  SELECT count(*) FROM pg_inherits;
  ```
- **Delta Vacuum**: When performing multiple streaming runs, clear stale metadata:
  ```bash
  docker compose exec -T jupyter python -c "from delta import *; ..." 
  ```

---

## 🔧 3. Troubleshooting Protocols (Incident Response)

### 🚨 Critical: Airflow/Jupyter Connectivity
If containers cannot talk to each other:
1. **Check Network**: `docker network ls` (Ensure `pde_platform_net` exists).
2. **Inspect Bridge**: `docker network inspect pde_platform_net` (Ensure all running demos are members).

### 🚨 High: Port Collisions
Since we use a **Symmetrical Modular Monolith**, we use offset ports:
- **Payments**: 5433
- **IoT Batch**: 5434
- **HR Applicants**: 5435
- **Airflow**: 8088

**Action**: If a demo fails to start, verify nothing is running on the specific host port using `netstat -ano | findstr <port>`.

---

## 📉 4. Cost Modeling ($0 Standard)

| Resource | Usage Tier | Cost (Monthly) |
| :--- | :--- | :--- |
| **Docker Engine** | Local (WSL2/Win) | **$0.00** |
| **GitHub Actions** | Free Tier (2,000 m/mo) | **$0.00** |
| **Storage (Delta/PG)** | Local Persistent Vol | **$0.00** |

**Enterprise Note**: If migrating to Cloud Run, apply the `cleanup_pr_cloudrun.sh` script to maintain the **$0 Budget Ceiling**.

---

## 📜 5. Definition of Done (Admin)
- [ ] `.\task.ps1 platform-status` returns `SUCCESS`.
- [ ] No hardcoded secrets in `.yml` or `.ps1`.
- [ ] Monitoring endpoints (8088, 8888, 8080) are reachable.
- [ ] Isolated networks are verified for each domain.
