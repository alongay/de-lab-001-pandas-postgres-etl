![Fraud-Ready Payments ETL](docs/assets/banner.png)

# de-lab-001-pandas-postgres-etl

Container-first, enterprise-style Data Engineering lab:
- Postgres in Docker Compose (localhost-only exposure)
- ETL as a Python module (`src/`)
- JupyterLab for exploration (`notebooks/`)
- Great Expectations quality gate (fail-fast)
- pytest unit tests (CI-ready)

## What this lab demonstrates
- Environment parity: same tooling in dev + CI (container-first)
- Secure configuration: secrets in `.env` (gitignored), no hardcoded credentials
- Production-ish pipeline layout: extract/transform/load separated into modules
- Data quality gating: pipeline fails non-zero when expectations fail
- Testing posture: unit tests that run without Postgres dependency (SQLite in-memory)

## Repo layout
```
.
├─ docker-compose.yml
├─ Dockerfile
├─ requirements.txt
├─ .env.example
├─ .env                 # gitignored
├─ pytest.ini
├─ src/
│  ├─ __init__.py
│  ├─ db.py
│  ├─ extract.py
│  ├─ transform.py
│  ├─ load.py
│  ├─ quality_ge.py
│  └─ etl_run.py
├─ notebooks/
│  └─ 01_extract_transform_load.ipynb
├─ tests/
│  ├─ conftest.py
│  ├─ test_transform.py
│  ├─ test_load.py
│  └─ test_quality_ge.py
├─ logs/                # gitignored (GE artifacts)
└─ docs/
   ├─ 01-sop-runbook.md
   ├─ 02-architecture.md
   ├─ 03-quality-and-testing.md
   ├─ 04-troubleshooting.md
   └─ 00-cheatsheet.md
```

## Security defaults (important)
- Postgres is bound to localhost only: `127.0.0.1:5432`
- JupyterLab is bound to localhost only: `127.0.0.1:8888`
- Jupyter requires a token stored in `.env`
- Containers run as a non-root user (uid/gid `10001`)
- No secrets are committed; `.env` is excluded by `.gitignore`

## Prerequisites
- Docker Desktop (Windows/macOS) or Docker Engine (Linux)
- PowerShell (Windows) or bash (Linux/macOS)
- Git (optional but recommended)

## Quickstart (PowerShell)
```powershell
# 1) Copy env template and set secrets
Copy-Item .env.example .env
notepad .env

# 2) Build and start services (Postgres + Jupyter)
docker compose up -d --build

# 3) Verify
docker compose ps

# 4) Run ETL (one-off)
docker compose run --rm etl

# 5) Run tests
docker compose run --rm etl pytest

# 6) Open Jupyter
# Visit: http://127.0.0.1:8888 (use token from .env)
```

## Quickstart (bash)

```bash
# 1) Copy env template and set secrets
cp .env.example .env
nano .env

# 2) Build and start services (Postgres + Jupyter)
docker compose up -d --build

# 3) Verify
docker compose ps

# 4) Run ETL (one-off)
docker compose run --rm etl

# 5) Run tests
docker compose run --rm etl pytest

# 6) Open Jupyter
# Visit: http://127.0.0.1:8888 (use token from .env)
```

## Documentation

* SOP / Runbook: `docs/01-sop-runbook.md`
* Architecture: `docs/02-architecture.md`
* Quality + Testing: `docs/03-quality-and-testing.md`
* Troubleshooting: `docs/04-troubleshooting.md`
* One-page cheat sheet: `docs/00-cheatsheet.md`

## One-command operations
- PowerShell: `.\task.ps1 up | etl | test | down`
- bash/macOS/Linux: `make up | etl | test | down`

## Non-goals

* Production scheduling (Airflow/Cloud Scheduler) — out of scope for this lab
* CI pipeline wiring — optional next step
* Upsert/staging swap load pattern — optional next step

## License

Internal training lab (adjust as needed).
