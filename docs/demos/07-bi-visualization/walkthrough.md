# Walkthrough: Demo 7 — Building the First Dashboard

Follow these steps to finalize **Lab 7** and build your first production-grade business intelligence dashboard.

## Prerequisites
- [x] Platform is Up: `.\task.ps1 platform-up`
- [x] Metabase is accessible: [http://localhost:3010](http://localhost:3010)

---

## Step 1 — Initial Calibration (The Wizard)
1.  Navigate to [http://localhost:3010](http://localhost:3010).
2.  Click **Let's get started**.
3.  **Language**: Choose your preferred language.
4.  **Admin Account**: Create your user (e.g., `admin@pde.lab`). 
    > [!TIP]
    > Write this down; Metabase handles its own auth and is separate from Airflow.

---

## Step 2 — Connecting the Warehouse
1.  Select **PostgreSQL** when asked to "Add your data".
2.  **Display Name**: `PDE Production Warehouse`
3.  **Host**: `postgres` (internal Docker hostname)
4.  **Port**: `5432`
5.  **Database name**: `de_workshop`
6.  **Username**: `de_user`
7.  **Password**: `de_password`
8.  **SSL**: Disable (local development).
9.  Click **Next** and then **Take me to Metabase**.

---

## Step 3 — Creating the "Cash Flow" Chart
1.  Click **+ New** -> **Question**.
2.  Select **Raw Data** -> **PDE Production Warehouse** -> **Public** -> **raw_payments**.
3.  **Filter**: (Optional) `status = CAPTURED`.
4.  **Summarize**: `Sum of Amount` grouped by `Txn Ts` -> `by hour`.
5.  Click **Visualize**.
6.  Change the chart type to **Line Chart**. You should see a spike corresponding to your Lab 2 and Lab 6 runs.
7.  Click **Save**. Add it to a new dashboard named **"Executive Platform Overview"**.

---

## Step 4 — Visualizing the "Chaos" (Lab 6 Audit)
1.  Click **+ New** -> **Question**.
2.  Select **Raw Data** -> **PDE Production Warehouse** -> **Public** -> **drift_reports**.
3.  **Summarize**: `Sum of Drift Instances` grouped by `Report Time` -> `by day`.
4.  Click **Visualize**.
5.  Choose **Bar Chart**.
    - If you ran the **Chaos Script** in Lab 6, you should see a significant bar on today's date.
6.  Click **Save** and add it to your dashboard.

---

## Step 5 — Final Polish
1.  Navigate to your **Executive Platform Overview** dashboard.
2.  Click **Edit Dashboard** (pencil icon).
3.  Resize and move your charts until they look like a professional suite.
4.  **Talking Point**: You can now prove to an interviewer that you built a pipeline that not only moves data but **self-audits** and **notifies stakeholders** through BI.

### Results: High-Fidelity Dashboard Suite
We now have a fully integrated BI layer covering Finance, HR, IoT, and Data Quality.

````carousel
![Executive Watchtower](file:///C:/Users/along/.gemini/antigravity/brain/835759b7-478e-4d3d-b1e2-b98c594c21bc/executive_watchtower_updated_insights_1773375767183.png)
Executive Watchtower: The central hub connecting all domain dashboards.
<!-- slide -->
![Talent Insights](file:///C:/Users/along/.gemini/antigravity/brain/835759b7-478e-4d3d-b1e2-b98c594c21bc/hr_dashboard_talent_insights_1773374828330.png)
Talent Insights: Applicant conversion and geographic distribution.
<!-- slide -->
![IoT Pulse](file:///C:/Users/along/.gemini/antigravity/brain/835759b7-478e-4d3d-b1e2-b98c594c21bc/iot_dashboard_pulse_1773374836643.png)
IoT Pulse: Real-time telemetry monitoring for pressure and temperature.
<!-- slide -->
![Data Quality Hub](file:///C:/Users/along/.gemini/antigravity/brain/835759b7-478e-4d3d-b1e2-b98c594c21bc/data_quality_hub_dashboard_1773375756607.png)
Data Quality Hub: Observability into quarantined records and storage partitions.
````

### Architecture of Visibility: Why tables appeared
Initially, only 2 tables were visible. Through debugging the "Last Mile" of production integration, we resolved:
1.  **Network Resolution**: Switched HR loader from `localhost` to `postgres` to allow container-to-container DB writing.
2.  **Quality Gate Tuning**: The IoT generator was producing "out of bounds" data (500°C+) which Great Expectations correctly diverted to quarantine. We adjusted the generator to produce "clean" data for production visuals.
3.  **Observability Layer**: We added the **Data Quality Hub** to make these "invisible" warehouse layers (Quarantine/Partitions) externally visible.

> [!TIP]
> **Interview Talking Point**: "I didn't just build dashboards; I built a multi-domain observability suite. When data didn't show up, I used the Quarantine tables to debug the ingestion logic, proving that the Great Expectations quality gates were working as intended."

---

### 💹 Advanced Analytics & Window Functions
To demonstrate "Data Scientist" level mastery, we've provided [**Advanced SQL Logic**](sql_catalog.md) for deeper insights:
*   **Revenue Growth %**: Tracks daily performance trends using `LAG()` window functions.
*   **Applicant Aging**: Calculates real-time cycle time to identify bottlenecks in hiring.
*   **Sensor Smoothing**: Filters high-frequency IoT noise via moving averages for cleaner dashboards.

---

### ⌨️ BI-as-Code: The Metabase API CLI
In senior-level production environments, all infrastructure is managed programmatically.
*   **[BI CLI Wrapper](../../scripts/metabase/metabase_api_cli.py)**: A Python implementation of the Metabase REST API.
*   **Capabilities**: Programmatically list dashboards, export configurations to JSON, and sync SQL logic from version control to the production server.
*   **Interview Power Point**: "I transitioned our BI layer into **BI-as-Code**, using a custom Python SDK to ensure our visualizations are version-controlled, reproducible, and decoupled from manual UI clicks."

---

**Congratulations!** You have completed the full Loop of Production Data Engineering across multiple distinct data domains.
