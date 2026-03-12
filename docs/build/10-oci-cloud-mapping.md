# OCI Cloud Mapping — From Local Demos to OCI Free Tier

## Purpose
This document maps the local demo platform to Oracle Cloud Infrastructure (OCI), with a focus on using **OCI Always Free** resources where practical and keeping the architecture close to production patterns.

This mapping covers:

- Demo 1: Payments Batch ETL
- Demo 2: IoT Batch Telemetry
- Demo 3: Real-Time IoT Streaming
- Demo 4: Orchestration & SLA Governance

---

## Executive summary

The local platform can be mapped to OCI in a staged way. A **strict 1 GB VM is not enough** for the full platform, especially for Kafka, Spark, and Airflow. OCI’s broader **Always Free Ampere A1 allocation** is the practical path because it provides up to **4 OCPUs and 24 GB memory total**, which can be split across multiple small VMs. OCI Always Free also includes **Object Storage**, **Monitoring/Logging/Notifications** allowances, and Always Free services are available for an unlimited period of time, subject to OCI limits and region capacity. :contentReference[oaicite:0]{index=0}

---

## Local-to-OCI service mapping

### Core platform mappings

| Local component | OCI equivalent | Why this mapping is used |
|---|---|---|
| Docker-hosted Postgres (warehouse / metadata) | OCI Compute-hosted PostgreSQL, or OCI Autonomous Database for managed DB use cases | Lets us keep the same relational patterns while moving state off the laptop |
| Kafka in Docker | OCI Streaming in a production-aligned design, or self-hosted Kafka on OCI Compute for lift-and-shift demos | OCI Streaming is the managed event backbone analogue; self-hosting is simpler for direct demo migration |
| Spark in Docker | OCI Data Flow for managed Spark, or self-hosted Spark on OCI Compute | Data Flow is the closest managed Spark equivalent; self-hosted Spark preserves the demo topology |
| Delta Lake on local disk | OCI Object Storage | Object Storage is the natural durable lake layer for Bronze/Silver/Quarantine assets |
| Airflow in Docker | Self-hosted Airflow on OCI Compute | Keeps orchestration patterns familiar and low-cost |
| Local logs / alerts | OCI Logging, Monitoring, Notifications | Matches observability and alerting patterns used in production :contentReference[oaicite:1]{index=1}

---

## OCI Always Free constraints that matter

### What matters most for this project
- OCI Always Free includes **Ampere A1 compute** up to **4 OCPUs and 24 GB memory total**, which is much more realistic for this project than trying to force everything onto a tiny instance. :contentReference[oaicite:2]{index=2}
- OCI Always Free includes **Object Storage**. In an Always Free-only state, OCI documentation says this is **20 GB combined** across Standard, Infrequent Access, and Archive tiers, with **50,000 Object Storage API requests per month**. :contentReference[oaicite:3]{index=3}
- OCI Always Free includes observability allowances such as up to **10 GB log storage per month**, plus monitoring/events/notifications free allowances documented by Oracle. :contentReference[oaicite:4]{index=4}
- Free Tier availability depends on **region capacity**, and Oracle notes that Always Free is available in commercial OCI regions where service availability exists. :contentReference[oaicite:5]{index=5}

### What this means in practice
- **1 GB alone is not enough** for the full platform.
- A **5-VM split** can work only if the combined VM shapes still fit within your Always Free compute allocation.
- Not all services should be left running all the time. Start only the parts needed for the current demo.

---

## Recommended 5-VM layout

This layout separates responsibilities and keeps the platform teachable.

### VM 1 — Batch ETL + DB + artifacts
**Purpose:** Run Demo 1 and Demo 2 batch flows with a relational sink and artifacts.

**Suggested contents**
- PostgreSQL
- Payments ETL runner
- IoT batch ETL runner
- Great Expectations artifacts
- small Jupyter or admin utilities only if needed

**Why this VM exists**
- Batch pipelines are easier to reason about when isolated from streaming.
- Database locality reduces complexity during early migration.

**OCI mapping**
- OCI Compute (Ampere A1)
- Optional Object Storage for artifacts and exports

---

### VM 2 — Kafka / event ingress
**Purpose:** Own the real-time event transport layer.

**Suggested contents**
- Kafka broker (self-hosted for direct demo parity)  
or
- Replace with OCI Streaming when moving closer to managed production patterns

**Why this VM exists**
- Event transport should be isolated from Spark compute.
- Keeps producer/consumer debugging clean.

**OCI mapping**
- OCI Compute if self-hosting Kafka
- OCI Streaming if using managed service

---

### VM 3 — Spark streaming compute
**Purpose:** Run Bronze and Silver streaming jobs.

**Suggested contents**
- Spark master
- Spark worker (combined for demo scale if needed)
- Bronze stream job
- Silver stream job

**Why this VM exists**
- Streaming compute is resource-hungry and should not compete with orchestration or DB services.
- This is the natural home for micro-batch processing.

**OCI mapping**
- OCI Compute for self-hosted Spark
- OCI Data Flow if you later move to managed Spark

---

### VM 4 — Orchestration & governance
**Purpose:** Run Airflow and platform governance logic.

**Suggested contents**
- Airflow webserver
- Airflow scheduler
- Airflow metadata DB if not externalized
- SLA monitor
- mock alerting or OCI Notifications integration

**Why this VM exists**
- Airflow should not compete with Spark and Kafka for memory.
- Keeps scheduling, retries, and monitoring clearly separated from processing engines.

**OCI mapping**
- OCI Compute
- OCI Notifications / Monitoring / Logging for alert paths :contentReference[oaicite:6]{index=6}

---

### VM 5 — Data lake / utility / observability edge
**Purpose:** Keep supporting services and tooling isolated.

**Suggested contents**
- light admin utilities
- optional reverse proxy / docs site
- lightweight observability scripts
- optional shared runner for screenshots, reports, or documentation generation

**Why this VM exists**
- Separates support functions from core data path services.
- Gives room for future observability or portfolio packaging work.

**OCI mapping**
- OCI Compute
- OCI Object Storage for reports, screenshots, and artifacts

---

## Why actions are taken this way

### Why split into 5 VMs
This is done for **resource isolation**, **failure isolation**, and **clearer operating boundaries**.

In real systems:
- databases should not fight Kafka for memory
- Spark should not fight Airflow for CPU
- orchestration should remain alive even when stream compute is busy

This separation also makes troubleshooting easier.

### Why not cram everything onto one small box
Kafka, Spark, and Airflow all have non-trivial memory footprints. Putting them together on an undersized host creates false failures that are caused by resource exhaustion instead of design problems.

### Why Object Storage is important
Delta-style Bronze/Silver/Quarantine storage belongs on durable object storage in cloud designs. That is what makes replayability, checkpointing, and cheap persistence viable.

### Why map managed services later
For learning and demo parity, self-hosting first is simpler:
- fewer moving parts
- easier comparison with local Docker
- easier troubleshooting

Once the architecture is proven, replacing self-hosted pieces with OCI managed services is more meaningful.

---

## Demo-by-demo OCI mapping

## Demo 1 — Payments Batch ETL
### Local
API + CSV → Python ETL → GE gate → PostgreSQL

### OCI
- ETL runner on VM 1
- PostgreSQL on VM 1 or moved to OCI database service
- GE artifacts to Object Storage
- Airflow on VM 4 triggers batch runs

### Why this is a good first cloud move
Batch ETL is the easiest workload to migrate and validate.

---

## Demo 2 — IoT Batch Telemetry
### Local
CSV/API → ETL → physical validation → partitioned relational storage → quarantine

### OCI
- IoT batch ETL on VM 1
- Partitioned PostgreSQL tables on VM 1 or managed DB later
- artifacts in Object Storage
- Airflow on VM 4 schedules and monitors runs

### Why this is next
It extends Demo 1 with partitioning and quarantine without introducing streaming complexity.

---

## Demo 3 — IoT Streaming
### Local
Producer → Kafka → Spark → Delta Bronze/Silver → Quarantine

### OCI
- producer on VM 5 or local client
- Kafka on VM 2, or OCI Streaming later
- Spark on VM 3, or OCI Data Flow later
- Delta paths on Object Storage
- Airflow on VM 4 monitors freshness/SLA, not the long-running stream lifecycle itself

### Why this comes later
Streaming is the most resource-sensitive and operationally noisy part of the platform.

---

## Demo 4 — Orchestration & SLA Governance
### Local
Airflow + shared network + DAG retries + streaming freshness monitor

### OCI
- Airflow on VM 4
- Monitoring / Logging / Notifications from OCI services where appropriate
- DAGs trigger batch flows and validate streaming freshness via Delta activity and job signals

### Why this is separated
Airflow is best used to orchestrate batch and monitor streaming health, not to own every long-running stream process directly.

---

## Networking model

### Recommended cloud network pattern
- One VCN
- One subnet for demo VMs if keeping it simple
- Restrict public exposure
- Only expose necessary UIs:
  - Airflow UI
  - Spark Master UI
  - optional docs/demo UI

### Service discovery
Use private IP or internal DNS names where possible.

### Why this matters
This mirrors the “shared internal platform network” pattern you already used locally.

---

## Storage model

### Recommended
- Delta Bronze/Silver/Quarantine on Object Storage
- local boot disks only for transient service runtime
- artifacts, screenshots, and reports stored externally

### Why
Cloud object storage is cheaper, more durable, and more production-aligned than storing lake assets on VM root disks.

---

## Security notes

### Minimum recommended controls
- keep secrets in `.env` equivalents or OCI secret mechanisms, not in code
- restrict public ports
- use least-privilege DB users
- separate clean vs quarantine outputs
- keep raw Bronze immutable
- do not log sensitive data unnecessarily

### Why
These are the same controls that make the local demos credible in cloud form.

---

## Operational guidance

### Start order
1. VM 1 batch/DB
2. VM 4 orchestration
3. VM 2 Kafka
4. VM 3 Spark
5. VM 5 support/utility services

### Migration order
1. Demo 1
2. Demo 2
3. Demo 4 control plane
4. Demo 3 streaming

### Why this order
It moves from lowest complexity to highest complexity.

---

## What “success” looks like

You know the OCI migration pattern is working when:
- batch ETL runs on schedule from Airflow
- GE artifacts are persisted outside the VM
- IoT batch data lands in partitioned storage
- Kafka receives live events
- Spark writes Bronze and Silver to cloud-backed storage
- Quarantine receives anomalies
- Airflow freshness checks alert when Silver stops advancing

---

## Final recommendation

For this project, OCI should be used as a **demo-scale cloud platform**, not as a place to run every service 24/7 at maximum footprint. A 5-VM separation is a good operating model conceptually, but it still needs to fit inside the real Always Free compute allowance. The practical strategy is:

- keep VMs small
- do not run all heavy services continuously
- move lake artifacts to Object Storage
- migrate batch first, streaming last
- replace self-hosted pieces with managed OCI services only after the cloud shape is stable

---

## OCI references used for this mapping
This plan is based on Oracle’s current Free Tier and service documentation, including Always Free availability, compute guidance, Object Storage allowances, and observability allowances. :contentReference[oaicite:7]{index=7}