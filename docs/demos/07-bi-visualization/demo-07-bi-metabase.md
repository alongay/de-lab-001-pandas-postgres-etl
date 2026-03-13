# Demo 7: Business Intelligence & Visualization (Metabase)

### 🎯 The Pitch
Data Engineering doesn't end when the table is loaded; it ends when the **Dashboard** is built. In this demo, we integrate **Metabase** as our open-source BI layer to visualize the results of our batch and streaming pipelines. 

This completes the **End-to-End Platform Lifecycle**:
`CSV/API Source` → `Validation (GE)` → `ETL (Pandas/SQL)` → `Orchestration (Airflow)` → `Observability (DuckDB)` → **`Visualization (Metabase)`**.

### 📉 Business Goals
- **Executive Insights**: Real-time view of `raw_payments` volume and value.
- **Operational Health**: Proactive monitoring of `drift_reports` for silent statistical pipeline failures.
- **Telemetry Trends**: Visualizing IoT sensor partitions and quarantine rates to detect sensor malfunctions.

### 🏗️ BI Architecture
- **Tool**: Metabase (Enterprise-grade Open Source BI).
- **Core Warehouse**: PostgreSQL (`de_workshop`).
- **Observability Hub**: Metadata extracts from the platform's auditing layer.
- **Connectivity**: Direct VPC-style link (via Docker networks) to the warehouse.

---

### 🚀 Technical Talking Points
- **"The Last Mile"**: Why data engineers must own the semantic layer to ensure dashboard accuracy.
- **Semantic Layer vs. Raw Tables**: Using Metabase to map raw schema to business-friendly terms.
- **Separation of Concerns**: Keeping BI internal storage (H2) separate from production data (Postgres).
- **Embedded Analytics**: How this setup scales to provide stakeholder-facing reports.

---
**Next steps:**
- [**Learning Guide**](learning_guide.md) — Technical concepts and exercises.
- [**Walkthrough**](walkthrough.md) — Step-by-step setup and dashboard build.
