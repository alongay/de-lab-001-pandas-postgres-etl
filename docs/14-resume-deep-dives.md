# 🏗️ Senior Platform Engineer Resume

## Profile
Senior Platform Engineer with a focus on **Developer Experience (DX)** and **Production Reliability**. Expert at containerizing complex data stacks and automating environment lifecycle management to ensure zero friction between development and production.

### 📈 Platform Performance Visualized (Data Proof)
| metric_name | legacy_baseline | pde_optimized | gain_impact |
| :--- | :--- | :--- | :--- |
| **Env Setup** | 120+ mins | < 5 mins | ⚡ 24x Speed Improvement |
| **Pipeline Recovery** | Manual Restart | Airflow Auto-Retry | 🔄 100% Reliability |
| **Connectivity** | Brittle (localhost) | Bridge (postgres) | 🛡️ zero_drift |

---

## Core Competencies
| Infrastructure | Automation | Orchestration |
| :--- | :--- | :--- |
| Docker & Docker Compose | PowerShell / Bash / Python | Apache Airflow DAGs |
| Service Mesh / Networking | CI/CD (GitHub Actions) | Cloud Run / GCR |
| IAM / Least Privilege | Idempotent System Setup | Health Monitoring |

---

## Professional Scenarios (Star Method)

### Scenario: "The Zero-Friction Sandbox"
*   **Task**: Create a reproducible development environment for a complex data stack (Spark, Airflow, Postgres, Kafka).
*   **Action**: Built a Docker-orchestrated platform and a custom automation controller (`task.ps1`) to handle setup, cleanup, and data seeding.
*   **Result**: Reduced new developer onboarding time from **1 day to < 5 minutes**.

### Scenario: "Cross-Container Networking Fix"
*   **Task**: Resolve intermittent connection failures between Python ETL services and the production Postgres warehouse.
*   **Action**: Refactored networking config from `localhost` to internal Docker bridge aliases (`postgres`) and implemented centralized connection pooling.
*   **Result**: Achieved **100% connectivity stability** and eliminated networking-related pipeline crashes.

---

## Experience Keywords for ATS
`Docker Compose`, `Idempotency`, `Infrastructure as Code`, `Automation Runner`, `Service-to-Service Networking`, `Container Health Checks`, `Orchestration Conductor`, `DevOps Maturity`.

---

# 🕵️ Senior Data Reliability Engineer (DRE) Resume

## Profile
Senior Data Reliability Engineer specializing in **Data Observability** and **Automated Quality Enforcement**. Passionate about transforming "black box" pipelines into transparent, observable systems where data quality is a first-class citizen.

### 🛡️ Observability & Quality Metrics (Data Proof)
| metric_name | legacy_manual_effort | pde_automated | reliability_gain |
| :--- | :--- | :--- | :--- |
| **Silent Failures** | High (User Reported) | 0% (Auto-Quarantine) | 💎 100% Integrity |
| **Validation Speed**| Hours (Post-hoc) | < 1s (inline GX) | ⚡ Near Real-Time |
| **Audit Coverage** | Sampling Only | 100% of Streams | 🔒 Full Compliance |

---

## Core Competencies
| Observability | Quality Enforcement | Reliability |
| :--- | :--- | :--- |
| Metabase BI Viz | Great Expectations (GX) | Airflow SLAs & Retries |
| SQL Audit Dashboards | Automated Quarantine | Partition Monitoring |
| Drift Detection | Schema Enforcement | Root Cause Analysis |

---

## Professional Scenarios (Star Method)

### Scenario: "The Invisible Data Quality Hub"
*   **Task**: Provide stakeholders with visibility into why certain data points were missing from production dashboards.
*   **Action**: Implemented an automated **Quarantine layer** and a corresponding Metabase **Quality Hub** dashboard to visualize intercepted records.
*   **Result**: Proved quality gate effectiveness and shifted focus from "missing data" to "preventing bad data."

### Scenario: "Physics-Based Quality Gates"
*   **Task**: Prevent "Data Poisoning" where sensor malfunction sends extreme values into the analytical warehouse.
*   **Action**: Integrated **Great Expectations** into the Spark Streaming engine to enforce physics-based constraints (e.g., Temperature 20-40°C).
*   **Result**: Eliminated manual data cleaning efforts and ensured **100% downstream accuracy**.

---

## Experience Keywords for ATS
`Data Reliability`, `Data Observability`, `Quality Gates`, `Quarantine Routing`, `SLA Compliance`, `Automated Auditing`, `Great Expectations`, `Metabase SQL`, `Pipeline Transparency`.
