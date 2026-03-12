# Demo Walkthrough — Fraud-Ready Payments Intake

This is a live demo script you can run in an interview or study session. It shows **enterprise signals**:
- **Container-first reproducibility**
- **Strict quality gating**
- **Unit and Integration tests**
- **Deterministic operator commands**

## 🚀 One-Command Demo
- **PowerShell**: `.\task.ps1 demo-payments`
- **Bash**: `make demo-payments`

> [!NOTE]
> This single command orchestrates the entire lifecycle: **Up → Generate Data → Happy Path → Inject Chaos → Prove Failure → Recover → Down.**

---

## 1. Start Services
**PowerShell**:
```powershell
.\task.ps1 up                   # Starts core lab (Jupyter)
.\task.ps1 demo-payments        # Orchestrates the isolated demo
```
**Bash**:
```bash
make up
```

**Expected Result**:
- **Postgres** is healthy and reachable.
- **JupyterLab** is running on `127.0.0.1:8888`.

## 2. Run Unit Tests (CI Parity)
**PowerShell**:
```powershell
.\task.ps1 test
```
**Bash**:
```bash
make test
```

> [!TIP]
> **Call-out**: Tests run in the exact same container image used by GitHub Actions (CI). This ensures that locally passing tests will also pass in the cloud.

## 3. Run Ingestion: CSV Source
Set `INGEST_SOURCE=csv` in your environment.

**PowerShell**:
```powershell
$env:INGEST_SOURCE="csv"; docker compose -f docker-compose.payments.yml run --rm payments-etl
```
**Bash**:
```bash
INGEST_SOURCE=csv docker compose -f docker-compose.payments.yml run --rm payments-etl
```

**Expected Logs**:
- **Extract** -> **Transform** -> **GE Gate** -> **Load** -> **Success**

## 4. Run Ingestion: API Source
Set `INGEST_SOURCE=api`.

**PowerShell**:
```powershell
$env:INGEST_SOURCE="api"; docker compose -f docker-compose.payments.yml run --rm payments-etl
```

**Expected Logs**:
- **API Extraction** successful -> **GE Gate Passed** -> **Loaded to Postgres**.

## 5. Audit the Quality Artifact
After a run, inspect the **Great Expectations** JSON report.

> [!IMPORTANT]
> **Talk Track**: "This artifact proves the data was validated against a strict contract. It details exactly which records passed and provides a cryptographic-like proof of quality before the data hits production."

## 6. Visual Exploration (Jupyter)
Open `http://127.0.0.1:8888` and use:
- `notebooks/payments/01_extract_transform_load.ipynb`

> [!NOTE]
> **Enterprise Pattern**: The notebook imports production `src/` modules. We never duplicate business logic inside a notebook; we use it as an **interactive layer** over the production codebase.

## 7. Shutdown
**PowerShell**:
```powershell
.\task.ps1 down
```

---

## 🎤 Demo "Talk Track"
- "This is a **Two-Source Ingestion Pipeline** standardized into a single raw contract."
- "We enforce a **Strict Quality Gate**; the pipeline fails with a non-zero exit code if integrity is breached."
- "We use a **Staging-First Promote Swap** to ensure atomic loads and avoid partial database states."
