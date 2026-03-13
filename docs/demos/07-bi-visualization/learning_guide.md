# Learning Guide: Demo 7 — Business Intelligence & The Semantic Layer

## Objective
To understand how data engineering principles (validation, standardization, orchestration) translate into **business value** through proactive visualization and the "Semantic Layer."

---

## 🔑 Key Technical Concepts

### 1. The "Last Mile" of Data Engineering
A data pipeline is only as good as the decisions it enables. While Lab 1-4 focused on the **Movement** and **Quality** of data, Lab 7 focuses on **Delivery**.
- **Data Engineering Role**: Ensuring the warehouse schema is "query-ready."
- **BI Role**: Translating technical columns into business dimensions (e.g., `txn_ts` -> `Transaction Date`).

### 2. Semantic Layers vs. Raw Tables
In this lab, we use Metabase to create a **Semantic Layer**. Instead of stakeholders querying `public.raw_payments` directly, they interact with a model where:
- Columns are human-readable.
- Formats are standardized (e.g., Currency symbols).
- Filters are pre-defined (e.g., "Exclude quarantined records").

### 3. Integrated Observability Dashboarding
One of the most powerful uses of BI for a Data Engineer is **Observability Visualization**. 
- **Passive**: Looking at a chart once a week.
- **Proactive**: Connecting Metabase to the `drift_reports` table (created in Lab 6) to see when pipeline health is degrading *before* it breaks down.

---

## 📂 Data Inventory
For this demo, we will be visualizing data from two distinct sources within the platform:

1.  **Main Warehouse (`de_workshop`)**:
    - `raw_payments`: Transaction volume, success rates, and values.
    - `raw_sensor_readings`: IoT telemetry trends and abnormal spikes.
2.  **Observability Layer**:
    - `drift_reports`: Historical statistical drift events (The "Red Alerts").
    - `quality_audit_log`: Historical GE failure logs.

---

## 🛠️ Lab Exercises

### Part A — Connecting the Dots
Connect Metabase to the PostgreSQL warehouse. This exercise teaches you how services communicate within a Dockerized VPC (`pde_platform_net`).

### Part B — The Executive View
Create a "Cash Flow" dashboard. 
- **Requirement**: Show total `amount` by `txn_ts` (hourly).
- **Challenge**: How do you handle multiple currencies? (Semantic layer logic).

### Part D — BI-as-Code & Version Control
Move from "Click-Ops" to "Git-Ops" for your visualization layer.
- **Requirement**: Use the custom **Metabase CLI** (`metabase_api_cli.py`) to export your dashboard configuration.
- **Challenge**: Document how treating a dashboard as a JSON file allows for peer reviews, rollback capabilities, and disaster recovery.

---

## 🏗️ BI-as-Code Architectural Pattern
Treating your visualization layer as code involves three core pillars:

1.  **Extraction**: Pulling UI configurations (cards, collections, dashboards) via REST API.
2.  **Versioning**: Storing those JSON configurations in the repository alongside the SQL logic.
3.  **Synchronization**: Re-applying configurations to new environments (Staging/Production) to ensure consistency.

*This pattern eliminates the common "The dashboard is broken in Prod" syndrome caused by manual UI edits.*

## 🎙️ Talking Points (Portfolio Ready)
- *"I implemented Metabase as a first-class citizen in the platform to close the loop between automated auditing and human decision-making."*
- *"I designed a semantic layer that shields stakeholders from raw pipeline complexity (like partitioning and quarantine logic) while delivering accurate metrics."*
- *"By visualizing metadata from our Great Expectations and Observability DAGs, I reduced the time-to-detection for statistical data drift."*

---
**Next Step:**
Follow the [**Step-by-Step Walkthrough**](walkthrough.md) to build these dashboards.
