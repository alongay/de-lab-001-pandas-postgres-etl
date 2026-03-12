![Fraud-Ready Payments ETL](docs/assets/banner.png)

# de-lab-001-pandas-postgres-etl

**Status: ✅ Production Symmetrical / Modular Monolith**

Container-first, enterprise-style Data Engineering lab:
- **Core Platform**: PostgreSQL 15 + JupyterLab
- **Domain Modules**: Isolated ETL and Logic in `src/` (Payments, IoT, Streaming)
- **Quality Gates**: Great Expectations (Batch) & Spark Quality Gates (Streaming)
- **Orchestration**: Apache Airflow (Enterprise Task Governance & Monitoring)
- **Persistence**: PostgreSQL (RDBMS) & Delta Lake (ACID Medallion)

## 📚 Documentation Hub
For a complete categorized index of all project materials (Build, SOPs, Architecture, and Demos), visit the **[Documentation Hub](docs/README.md)**.
- **Runbook**: [Daily Data Tasks](docs/operations/01-sop-runbook.md)
- **Admin Guide**: [Platform Maintenance & Governance](docs/operations/02-admin-guide.md) (SOP)

## 🏗️ Repository Architecture
The lab uses a **Symmetrical Modular Monolith** pattern:
```
.
├─ src/
│  ├─ core/             # Shared utilities (db.py)
│  ├─ payments/         # Demo 1: Fraud-Ready Payments
│  ├─ iot/              # Demo 2: IoT Batch Telemetry
│  ├─ streaming/        # Demo 3: Enterprise Streaming
│  ├─ hr/               # Demo 5: HR Compliance & PII
│  └─ orchestration/     # Demo 4: Platform Symmetrization
├─ scripts/             # Operational & Data Gen scripts (Modular)
├─ notebooks/           # Domain-specific exploration (Modular)
├─ data/                # Persistence layers (Payments, IoT, Delta, HR)
├─ logs/                # Audit & Quality artifacts
└─ docs/                # SOPs, Runbooks, and Demos
```

## 🚀 Quickstart (The 6-Step Demo)

### 1) Environment Setup
```powershell
Copy-Item .env.example .env     # (PowerShell)
cp .env.example .env            # (bash)
```

### 2) Provision Infrastructure
```powershell
.\task.ps1 up                   # Build & start core services
```

### 3) Run a Domain Demo (One-Command)
Choose a demo project to orchestrate:
- `.\task.ps1 demo-payments`    # Financial ingestion flow
- `.\task.ps1 demo-iot`         # Batch time-series flow
- `.\task.ps1 demo-iot-stream`  # Real-time event flow (Kafka/Spark)
- `.\task.ps1 demo-orchestration` # Enterprise Platform Governance (Airflow)
- `.\task.ps1 demo-hr`          # Privacy & Compliance flow (PII Redaction)

### 4) Verify Infrastructure
```powershell
.\task.ps1 ps                   # See healthy containers
```

### 5) Run Unit Tests
```powershell
.\task.ps1 test                 # Runs pytest in the ETL env
```

### 6) Interactive Exploration
- **Jupyter**: Visit `http://127.0.0.1:8888` (Use token from `.env`)
- **Spark UI**: Visit `http://127.0.0.1:8080` (During streaming)

## 🎤 Interview "Gold" (Senior DE Signals)
Explain how this lab solves production-level problems:
1. **Medallion Architecture**: Using Bronze/Silver/Quarantine to ensure data lineage.
2. **Standardization**: Enforcing strict UTC and standard contract casting across sources.
3. **Infrastructure as Code**: Using hyphenated service naming for Java/RFC 1123 compliance.
4. **Resilience**: In-stream quality gates and batch-level Great Expectations gates.
