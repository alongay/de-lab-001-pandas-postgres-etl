# Demo 7: Business Intelligence & Visualization

**Status: ✅ Active (Lab 7 Completed)**

### 🎯 The Pitch
Data Engineering doesn't end at the table; it ends at the **Dashboard**. In this demo, we integrate **Metabase** as our open-source BI layer to visualize the results of our batch and streaming pipelines. 

---

### 📉 Documentation Suite
To master the BI layer, follow these documents in order:

1.  [**The Pitch / Overview**](demo-07-bi-metabase.md) — Why BI matters and how it fits into the lifecycle.
2.  [**Learning Guide**](learning_guide.md) — Technical concepts: Semantic layers, BI vs Observability.
3.  [**Walkthrough**](walkthrough.md) — Step-by-step UI guide for building dashboards.

---

### 🛠️ BI Engineering Assets
To move beyond "point-and-click" BI, we have formalized our visualization logic:

*   [**SQL Catalog**](sql_catalog.md) — Version-controlled source of truth for all dashboard queries.
*   [**Connectivity Script**](../../scripts/metabase/verify_bi_connectivity.py) — Automated verification of the Warehouse-to-Metabase bridge.

---

### 🏗️ BI Architecture
- **Tool**: Metabase (Dockerized on Port 3010).
- **Core Warehouse**: PostgreSQL (`de_workshop`).
- **Observability Hub**: Metadata extracts from our auditing layer.
