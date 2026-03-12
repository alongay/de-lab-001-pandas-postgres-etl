# Interview Q&A: Platform & Data Reliability Engineering

This document curates **high-impact interview questions and answers** based on the architecture and patterns implemented in this lab. It serves as a study guide for **Platform/DRE roles**.

---

## 🏗️ 1. Architecture & Design Patterns

### Q: Why did you choose a "Batch Quarantine Pattern" over simply failing the pipeline?

> [!TIP]
> **A:** In production, **data loss is often worse than data delay**. By routing bad batches to a `quarantine` table instead of just dropping them or halting the entire system, we achieve three things:
> - **Operational Resilience**: The pipeline keeps moving for other valid batches.
> - **Auditability**: We preserve the exact payload that failed for root-cause analysis.
> - **Recovery**: Once the upstream issue is fixed, we have the records ready for reprocessing.

### Q: Explain the benefit of Declarative Partitioning in an IoT context.

> [!IMPORTANT]
> **A:** IoT data is high-velocity and grows linearly with time. Partitioning by **reading_ts** allows the database to:
> - **Scan Pruning**: Queries for a specific month only touch that partition, drastically reducing I/O.
> - **Efficient Deletion**: "Aging out" data becomes a metadata operation (`DROP TABLE partition_name`) rather than a heavy `DELETE` command.
> - **Parallelism**: Multiple partitions can be scanned in parallel by the Postgres query planner.

---

## 🛡️ 2. Data Quality & Reliability

### Q: How do you handle "Sensor Drift" or hardware faults in your pipeline?

> [!CAUTION]
> **A:** We implement **Physical Integrity Gates** using **Great Expectations**. Unlike a simple schema check, we encode the **"Laws of Physics."** This prevents corrupted data from poisoning downstream ML models.

### Q2: Why is the source code organized into `src/payments`, `src/iot`, and `src/streaming`?
**Answer**: This is a **Modular Monolith** pattern. By grouping logic into domain-driven modules, we ensure that:
- **Dependency Isolation**: Changes to the IoT quality gate don't accidentally break the Payments logic.
- **Entrypoint Clarity**: Each demo has a dedicated **Runner** (e.g., `etl_run_payments.py`) while sharing core utilities like `db.py`.
- **Developer Onboarding**: New engineers can focus on a single domain without navigating a flat, confusing directory.

### Q3: How do you handle database connections across these modules?
**Answer**: We use a **Shared Core** utility (`src/db.py`). It provides a standard method to retrieve **SQLAlchemy Engines** using environment variables, ensuring that all modules follow the same security and performance (pooling) standards.
### Q: Why use a composite index on `(device_id, reading_ts)` for IoT telemetry?

> [!NOTE]
> **A:** Time-series queries almost always filter by a specific entity (**Device ID**) and a range of time. A composite index allows the database to locate the device's start point and perform a **high-speed sequential scan** for the requested time range.

### Q: Why do you have separate `docker-compose` files for each demo?

> [!TIP]
> **A:** This is **Infrastructure Symmetrization**. By isolating each business domain into its own stack, we ensure:
> - **Port Collision Avoidance**: We can run the Payments and HR demos simultaneously on different offset ports (`5433` vs `5435`).
> - **Fault Isolation**: A corrupted database volume in the IoT domain doesn't impact the Payments domain.
> - **Deployment Parity**: It mimics a microservices architecture where each service owns its own persistence layer and infrastructure lifecycle.
> - **Clean Auditing**: Volume and network names are scoped to the domain (e.g., `pde_payments_net`), making platform-wide logging and monitoring much cleaner.

---

## ⚙️ 3. Operations & CI/CD

### Q: How do you ensure your local development environment matches production?
**A:** Through **Containerization (Docker)** and a **Task Runner script (`task.ps1`)**.
- Every dependency is locked in the **Dockerfile**.
- The `demo-iot` task automates the exact sequence used in production, eliminating **"it works on my machine"** syndrome.

### Q: What is the $0 Budget Ceiling principle you followed?
**A:** It’s a design constraint to ensure the lab is **cost-optimized**. By using local Docker volumes and open-source tools, we proof-of-concept heavy enterprise patterns without incurring cloud provider costs.

---

## 🏗️ 4. Advanced Streaming & Medallion Architecture

### Q: Why use `foreachBatch` in your Silver streaming pipeline?

> [!TIP]
> **A:** `foreachBatch` allows us to implement **Multi-Sink output** within a single streaming query. Instead of running two separate queries (which would double the compute cost and Kafka reads), we process the micro-batch once and use standard Spark Dataframe API to write to both the **Silver** (Clean) and **Quarantine** (Anomaly) Delta tables. This ensures **atomic consistency** across both sinks.

### Q: You encountered a `JAVA_GATEWAY_EXITED` error during Spark deployment. How did you resolve it?

> [!IMPORTANT]
> **A:** This was a **Runtime Dependency** issue. The base `python:3.11-slim` image lacks the Java Virtual Machine (JVM) required by PySpark. I resolved this by refactoring the **Dockerfile** to install `openjdk-17-jre-headless`. I also learned to pin the base image to a stable release like `bookworm` to avoid "dependency drift" in experimental Debian branches (like `trixie`).

### Q: Why do Delta Lake transaction logs (`_delta_log`) trigger "End of file expected" errors in standard JSON validators?

> [!NOTE]
> **A:** Delta logs use **JSONL (JSON Lines)**, not a standard JSON array. Each line is a separate atomic operation (e.g., `commitInfo`, `add`, `remove`). This format allows Spark to **append operations** efficiently without re-writing the entire commit file, supporting the high-frequency atomic guarantees required by streaming pipelines.

---

## 🎯 5. Domain Comparisons

### Q: How does your approach to "Financial Correctness" differ from "Physical Reality"?
- **Demo 1 (FinTech)** focus: **Canonical Conflict Resolution** (UPSERT logic).
- **Demo 2 (IoT)** focus: **Anomaly Isolation** (Filtering noise and drift).

---

## 🏗️ 5. Real-World Infrastructure "War Stories"

### Q: Have you ever encountered a situation where a service worked in Docker but failed inside the container runtime?

> [!IMPORTANT]
> **A:** Yes, during the Spark Streaming implementation. We encountered a **Java URI Compliance** issue. While Docker allows underscores (`_`) in service names, Spark's Java runtime strictly enforces **RFC 1123**. This meant `iot_spark_master` was rejected as an "Invalid Master URL." I refactored the entire infrastructure to use hyphenated names, ensuring cross-platform protocol compliance.

### Q: How do you handle "Dependency Drift" when a public container registry changes its tagging policy?

> [!CAUTION]
> **A:** We recently faced this with **Bitnami**. They moved versioned tags to a `bitnamilegacy` repository without a redirect. Our pipeline failed to resolve the images. I resolved this by:
> 1. Updating the `image:` tags to the legacy registry.
> 2. Documenting the change in the **Troubleshooting SOP**.
> 3. Implementing a local **Docker Image Caching** strategy to prevent future registry disruptions from breaking the dev loop.

### Q: What's a common pitfall when writing cross-platform automation scripts (PowerShell/Bash)?

> [!WARNING]
> **A:** **Character Encoding (BOM)** conflicts. We found that PowerShell scripts saved with UTF-8 BOM can misparse string terminators if they contain complex emojis or special characters. I solved this by standardizing on **Pure UTF-8 (No BOM)** and using plain-text status indicators for mission-critical automation.

---

---

## 🛡️ 6. Data Privacy & Compliance (Demo 5)

### Q: How do you handle PII (Personally Identifiable Information) in system logs?

> [!CAUTION]
> **A:** We implement **In-Memory Redaction**. By using a dedicated `redact_pii` utility in our transformation logic, we scrub sensitive fields (like emails and names) before any logging occurs. This prevents PII from leaking into system logs (Elasticsearch/Splunk/CloudWatch), reducing audit scope and complying with **GDPR/CCPA privacy standards**.

### Q: Explain how you enforce Data Sovereignty in a global pipeline.

> [!IMPORTANT]
> **A:** We use **Negative Load Gates**. In our HR Demo, we cross-reference incoming country codes against an **ISO Allowed-List**. Any records from non-compliant regions are blocked from the main table and moved to a **Compliance Quarantine** for manual review, ensuring legal data residency boundaries are respected.

---

> [!NOTE]
> This document is updated dynamically as we implement new demos. 
