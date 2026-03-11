# Demo Project 1 — Payments Intake + Canonical View + Chaos Run

This demo teaches an enterprise-grade ingestion pattern:
- Multi-source intake (API mock + CSV drop)
- Standardization into `raw_payments`
- Great Expectations (GE) strict quality gate
- Canonical view enforcing “CSV wins”
- Chaos Engineering: inject bad data, prove gate blocks, recover cleanly

## Preconditions
- Docker Compose stack works (`postgres`, `etl`, `jupyter`)
- `.env` exists (copied from `.env.example`) and contains:
  - `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`
  - `JUPYTER_TOKEN`
  - `INGEST_SOURCE`
  - `API_URL` (file:// mock or https)
  - `CSV_PATH`

## Dataset Locations (inside repo)
- API mock JSON: `data/payments/transactions.json`
- CSV drop: `data/payments/transactions_daily.csv`

Inside containers, repo is mounted at `/app`, so file URLs should use:
- `API_URL=file:///app/data/payments/transactions.json`

---

# Part A — Start services

### PowerShell
```powershell
.\task.ps1 up
```

### bash

```bash
make up
```

Expected:

* Postgres healthy
* Jupyter available at `http://127.0.0.1:8888`

---

# Part B — Clean slate (demo hygiene)

Reset the demo table (deterministic results).

### PowerShell / bash

```bash
docker exec -it pde_postgres_15 sh -lc "psql -U $POSTGRES_USER -d $POSTGRES_DB -c 'TRUNCATE TABLE raw_payments;'"
```

If `$POSTGRES_USER` / `$POSTGRES_DB` aren’t exported in your host shell, use the known lab values:

```bash
docker exec -it pde_postgres_15 sh -lc "psql -U de_user -d de_workshop -c 'TRUNCATE TABLE raw_payments;'"
```

---

# Part C — Happy path run (both sources)

Run the pipeline in BOTH mode.

### PowerShell

```powershell
$env:INGEST_SOURCE="both"; docker compose run --rm etl
```

### bash

```bash
INGEST_SOURCE=both docker compose run --rm etl
```

Expected:

* GE gate passes (e.g., 11/11)
* ETL finishes successfully

Verify raw table has both partner versions:

```bash
docker exec -it pde_postgres_15 sh -lc "psql -U de_user -d de_workshop -c 'SELECT txn_id, partner_id, status, amount FROM raw_payments ORDER BY txn_id, partner_id;'"
```

You should see 2 rows per `txn_id` (partner_api + partner_csv), if both sources contain the same `txn_id`.

---

# Part D — Create canonical view (CSV wins)

Goal: downstream consumers want ONE best record per `txn_id`.

Rule:

1. prefer `partner_csv`
2. tie-breaker: newest `ingested_at`

Create or replace the view:

```bash
docker exec -it pde_postgres_15 sh -lc "psql -U de_user -d de_workshop -c \"CREATE OR REPLACE VIEW raw_payments_canonical AS
SELECT DISTINCT ON (txn_id)
  txn_id,
  partner_id,
  status,
  amount,
  currency,
  txn_ts,
  ingested_at
FROM raw_payments
ORDER BY
  txn_id,
  CASE WHEN partner_id = 'partner_csv' THEN 2 ELSE 1 END DESC,
  ingested_at DESC;\""
```

Verify canonical output:

```bash
docker exec -it pde_postgres_15 sh -lc "psql -U de_user -d de_workshop -c \"SELECT txn_id, partner_id, status, amount
FROM raw_payments_canonical
ORDER BY txn_id;\""
```

Expected:

* For overlapping transactions, `partner_csv` row wins.

---

# Part E — Chaos Engineering run (inject bad data)

## E1) Inject a negative amount into CSV

Edit `data/payments/transactions_daily.csv` and set one amount to a negative value (e.g., -75.50).

Example row:

```csv
TXN-30002,ACCT-9002,-75.50,USD,CAPTURED,2026-03-01T12:35:56Z
```

## E2) Run CSV-only ingestion to isolate the failure

### PowerShell

```powershell
$env:INGEST_SOURCE="csv"; docker compose run --rm etl
```

### bash

```bash
INGEST_SOURCE=csv docker compose run --rm etl
```

Expected:

* Pipeline fails non-zero
* Error references GE artifact path:

  * `logs/ge_validation_<timestamp>.json`

List artifacts:

### PowerShell

```powershell
Get-ChildItem .\logs | Sort-Object LastWriteTime -Descending | Select-Object -First 5
```

### bash

```bash
ls -la logs/ | head
```

Inspect which expectation failed (PowerShell quick parse):

```powershell
$latest = Get-ChildItem .\logs\ge_validation_*.json | Sort-Object LastWriteTime -Descending | Select-Object -First 1
(Get-Content $latest.FullName | ConvertFrom-Json).results |
  Where-Object { $_.success -eq $false } |
  Select-Object -First 5 |
  Format-List
```

Expected failure:

* `expect_column_values_to_be_between` for `amount` with `min_value=0`

---

# Part F — Recovery

## F1) Fix CSV amount back to valid (e.g., 15.00)

Re-run CSV-only:

### PowerShell

```powershell
$env:INGEST_SOURCE="csv"; docker compose run --rm etl
```

### bash

```bash
INGEST_SOURCE=csv docker compose run --rm etl
```

Expected:

* GE gate passes
* ETL finishes successfully

---

# Part G — Shutdown

### PowerShell

```powershell
.\task.ps1 down
```

### bash

```bash
make down
```

---

## Talking points (interview-ready)

* “We ingest from multiple feeds and standardize to a single raw contract.”
* “We enforce strict quality gates; invalid partner data never lands.”
* “We retain all raw versions for auditability.”
* “We provide a canonical view for consumers with deterministic conflict resolution.”
* “We use container-first dev for environment parity and CI reliability.”
