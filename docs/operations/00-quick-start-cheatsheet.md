# ⚡ PDE Platform: Quick-Start & Shutdown Cheatsheet

Use this guide to manage the lifecycle of your Data Engineering Platform gracefully.

---

## 🚀 Cold Start (The "Professional" Way)
Run these commands to bring up the **entire ecosystem** (Airflow, Metabase, Postgres, Spark).

1.  **Initialize Infrastructure**:
    ```powershell
    .\task.ps1 platform-init
    ```
2.  **Start Orchestration Platform**:
    ```powershell
    .\task.ps1 platform-up
    ```
    - **Airflow**: [http://localhost:8088](http://localhost:8088)
    - **Metabase**: [http://localhost:3010](http://localhost:3010)

3.  **Run All Demos (via Orchestration)**:
    Once the platform is up, you can trigger individual DAGs in Airflow or run isolated demos below.

---

## 🕹️ Isolated Domain Demos
Each command starts a specific, isolated pipeline stack.
> [!NOTE]
> Running `demo-payments` only starts the Payments pipeline. It does **not** start the full Airflow/Metabase platform unless you use the commands above.

| Domain | Command | What it does |
| :--- | :--- | :--- |
| **Finance** | `.\task.ps1 demo-payments` | Starts Payments stack + Generates Chaos data. |
| **HR** | `.\task.ps1 demo-hr` | Starts HR stack + PII Redaction verification. |
| **IoT Batch** | `.\task.ps1 demo-iot` | Starts Batch IoT pipeline. |
| **Streaming** | `.\task.ps1 demo-iot-stream` | Starts Kafka + Spark + Delta Lake Medallion. |
| **Observability**| `.\task.ps1 demo-observability`| Runs Statistical Drift & Audit Hub. |

---

## 🛑 Graceful Shutdown
Always shut down gracefully to avoid database corruption or orphaned containers.

1.  **Stop All Platform Services**:
    ```powershell
    .\task.ps1 platform-down
    ```
2.  **Stop Individual Domain Demos**:
    If you ran a specific demo like `demo-payments`, simply run:
    ```powershell
    .\task.ps1 down
    ```

---

## 🛡️ Security & Shielding (Vulnerability SOP)
Maintain a **Zero-Trust** posture for your containers and data.

1.  **Vulnerability Scanning**:
    ```powershell
    .\scripts\security\scan_vulnerabilities.ps1
    ```
2.  **Secret Scrubbing**:
    ```powershell
    .\scripts\security\scan_secrets.ps1
    ```
3.  **Patching Policy**:
    - If a **High/Critical CVE** is detected in a base image (e.g., `postgres`), update the version in `docker-compose.yml` and run `.\task.ps1 rebuild`.
    - **Never** commit `.env` or plain-text passwords to GitHub.

---

## 🧹 The "Fresh Start" (Deep Clean)
If you want to wipe all raw data, database volumes, and logs to start completely from scratch:
```powershell
.\task.ps1 clean
```

**Project Health: MISSION ACCOMPLISHED** 🚀🏙️💎🏁
