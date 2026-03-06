# SOP / Runbook: Fraud-Ready Payments ETL

Welcome to the Fraud-Ready Payments ETL pipeline! This runbook is written to onboard you into our container-first environment. Our goal is to run enterprise-grade data engineering patterns directly on your local machine exactly as they run in production.

Below are the step-by-step instructions for getting the environment running, exploring the data, and executing the pipeline.

---

## 1. Clone and Initialize the Repository
**What you are doing:** Downloading the source code to your local machine.
**Why:** You need the localized pipeline logic, Docker Compose manifests, and Jupyter environments to begin work.

### PowerShell & bash
```bash
git clone <REPO_URL>
cd de-lab-001-pandas-postgres-etl
```

---

## 2. Secure Configuration (`.env`)
**What you are doing:** Duplicating the configuration template and assigning real, secure credentials.
**Why:** Enterprise environments strictly isolate secrets (like database passwords and API keys) from the source code. The `.env` file is heavily `.gitignore`'d to prevent credential leaks.

1. **Copy the template:**
   - *PowerShell:* `Copy-Item .env.example .env`
   - *bash:* `cp .env.example .env`
2. **Edit `.env` and configure your credentials:**
   - `POSTGRES_USER` & `POSTGRES_PASSWORD` (Your local DB access)
   - `JUPYTER_TOKEN` (Create a random secure phrase to lock your Jupyter instance)
   - `INGEST_SOURCE` (Choose `api`, `csv`, or `both`)

---

## 3. Build and Start the Infrastructure
**What you are doing:** Booting up the PostgreSQL database and the JupyterLab server as persistent background services.
**Why:** The ETL script requires an active database to load data into. JupyterLab acts as your interactive exploration environment.

### PowerShell & bash
```bash
docker compose up -d --build
```

**Verify Health:**
Run `docker compose ps`. You should expect to see the `pde_postgres_15` container explicitly marked as `(healthy)` and the `pde_jupyter_lab` marked as `Up`.

---

## 4. Log into JupyterLab (Data Profiling)
**What you are doing:** Accessing the interactive data exploration UI.
**Why:** Before writing rigid ETL scripts, Data Engineers use tools like Jupyter to interactively profile raw datasets, discover edge cases, and define validation rules.

1. Open your browser to: `http://127.0.0.1:8888`
2. Paste the `JUPYTER_TOKEN` you defined in your `.env` file.

*Tip: If you forgot your token, run `docker exec -it pde_jupyter_lab jupyter server list` to reveal it.*

---

## 5. Run the ETL Pipeline
**What you are doing:** Executing the modular Python ingestion script.
**Why:** This spins up a transient (temporary) container, executes the `src/etl_run.py` script, and destroys itself upon completion. This guarantees a perfectly sterile, reproducible execution environment every single time.

### PowerShell & bash
```bash
docker compose run --rm etl
```

**Expected Output:**
You will see chronological logs confirming the Extraction, strict Great Expectations validations (enforcing numeric ranges and expected transaction statuses), and finally a staged UPSERT replacing the `raw_payments_stg` staging table before merging safely into `raw_payments`. It should end with `ETL pipeline finished successfully` (Exit Code 0).

---

## 6. Run the CI Unit Tests
**What you are doing:** Exercising the `pytest` suite within the Docker container.
**Why:** To ensure changes to the schema or logic haven't broken the pipeline. By running it inside the container, you guarantee exact parity with the GitHub Actions CI pipeline.

### PowerShell & bash
```bash
docker compose run --rm etl pytest
```

**Expected Output:**
All tests pass cleanly. (e.g., `9 passed`)

---

## 7. Teardown & Clean Up
**What you are doing:** Shutting down the background Docker services to free up RAM/CPU.
**Why:** General hygiene. Data inside Postgres is safely persisted to a persistent Docker Volume (`postgres_data`) so you won't lose your ingested rows.

### PowerShell & bash
```bash
docker compose down
```

### Optional: The "Nuke" Command (Destructive)
If you wish to completely wipe the Postgres database and start entirely fresh:
```bash
docker compose down -v
```
*(Warning: This irreversibly deletes the `postgres_data` volume).*
