# Demo Walkthrough — Fraud-Ready Payments Intake (5–8 minutes)

This is a live demo script you can run in an interview or study session. It shows enterprise signals:
- container-first reproducibility
- strict quality gate
- tests
- deterministic operator commands

## One-command demo
- PowerShell: `.\task.ps1 demo-payments`
- bash: `make demo-payments`

This runs: up → generate demo data → reset table → happy path → inject chaos → prove GE failure → recover → down

---

## Prep (once)
Ensure `.env` exists:
- PowerShell: `Copy-Item .env.example .env`
- bash: `cp .env.example .env`

Edit `.env` to set:
- `INGEST_SOURCE`
- `API_URL` (use `file://` for local mock or https for live endpoint)
- `CSV_PATH`
- `POSTGRES_*` values
- `JUPYTER_TOKEN`

## 1) Start services
PowerShell:
```powershell
.\task.ps1 up
```

bash:
```bash
make up
```

Expected:

* Postgres is healthy
* Jupyter is up on `127.0.0.1:8888`

## 2) Run unit tests (CI parity)

PowerShell:

```powershell
.\task.ps1 test
```

bash:

```bash
make test
```

Call-out:

* Tests run in the same container image CI uses.
* Includes transform/gate/load unit tests (load uses SQLite in-memory to avoid DB dependency).

## 3) Run ingestion: CSV only

Set:

* `INGEST_SOURCE=csv`
* Ensure `CSV_PATH` points to your inbound CSV

PowerShell:

```powershell
$env:INGEST_SOURCE="csv"; docker compose run --rm etl
```

bash:

```bash
INGEST_SOURCE=csv docker compose run --rm etl
```

Expected logs:

* Extract -> Transform -> GE Gate -> Load -> Success

## 4) Run ingestion: API only (local mock or https)

Set:

* `INGEST_SOURCE=api`
* `API_URL=file:///app/data/payments/transactions.json` (container path) OR a real https endpoint

PowerShell:

```powershell
$env:INGEST_SOURCE="api"; docker compose run --rm etl
```

bash:

```bash
INGEST_SOURCE=api docker compose run --rm etl
```

Expected logs:

* Extract -> Transform -> GE Gate -> Load -> Success

## 5) Show the quality artifact

After a run, show:

* `logs/ge_validation_<timestamp>.json`

PowerShell:

```powershell
Get-ChildItem .\logs
```

bash:

```bash
ls -la logs/
```

Explain what it proves:

* `success: true/false`
* how many expectations were evaluated and passed
* exactly which rule fails (if any)

## 6) (Optional) Show Jupyter exploration

Open:

* `http://127.0.0.1:8888` (token from `.env`)
  Use notebook:
* `notebooks/01_explore_payments.ipynb`

Explain enterprise pattern:

* Notebook imports `src/` modules (no duplicated “prod logic” in notebook).

## 7) (Optional) Prove data landed in Postgres

Run a quick count by partner:

PowerShell:

```powershell
docker exec -it pde_postgres_15 sh -lc "psql -U `$POSTGRES_USER -d `$POSTGRES_DB -c 'SELECT partner_id, COUNT(*) FROM raw_payments GROUP BY partner_id;'"
```

bash:

```bash
docker exec -it pde_postgres_15 sh -lc "psql -U \"$POSTGRES_USER\" -d \"$POSTGRES_DB\" -c 'SELECT partner_id, COUNT(*) FROM raw_payments GROUP BY partner_id;'"
```

## 8) Shutdown

PowerShell:

```powershell
.\task.ps1 down
```

bash:

```bash
make down
```

---

## Demo “talk track” (short)

* “This is a two-source ingestion pipeline (API + CSV) standardized into a single raw contract.”
* “We enforce a strict Great Expectations gate; pipeline fails non-zero if data is invalid.”
* “We load with a staging-first promote swap to avoid partial states.”
* “Unit tests run in-container for CI parity; integration smoke test runs on main.”
