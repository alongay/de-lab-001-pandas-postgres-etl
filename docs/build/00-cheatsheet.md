# Cheat Sheet — de-lab-001-pandas-postgres-etl

## Start / Stop
### PowerShell
```powershell
# Why: Compiles the custom Python Dockerfile and starts PostgreSQL/Jupyter in the background.
docker compose up -d --build

# Why: Verifies that pde_postgres_15 is (healthy) before running pipelines.
docker compose ps

# Why: Stops and cleanly destroys all active containers.
docker compose down
```

### bash

```bash
# Why: Compiles the custom Python Dockerfile and starts PostgreSQL/Jupyter in the background.
docker compose up -d --build

# Why: Verifies that pde_postgres_15 is (healthy) before running pipelines.
docker compose ps

# Why: Stops and cleanly destroys all active containers.
docker compose down
```

## Run ETL

The ETL pipeline evaluates the `INGEST_SOURCE` environment variable to determine which partners to ingest (`api`, `csv`, or `both`).

### PowerShell

```powershell
# Run API extraction only
$env:INGEST_SOURCE="api"; docker compose run --rm etl

# Run CSV extraction only
$env:INGEST_SOURCE="csv"; docker compose run --rm etl

# Run BOTH sources and consolidate them into the raw staging table
$env:INGEST_SOURCE="both"; docker compose run --rm etl
```

### bash

```bash
# Run API extraction only
INGEST_SOURCE=api docker compose run --rm etl

# Run CSV extraction only
INGEST_SOURCE=csv docker compose run --rm etl

# Run BOTH sources and consolidate them into the raw_payments table
# Why: Using --rm ensures this transient data engineering container destroys itself immediately after loading Postgres, preventing memory leaks or state corruption between runs.
INGEST_SOURCE=both docker compose run --rm etl
```

## Run Tests

The pytest suite must be run inside the container to ensure environmental parity with CI. It includes tests for individual extraction modes, staging UPSERT logic, transformations, and the Great Expectations quality gate.

### PowerShell

```powershell
docker compose run --rm etl pytest
```

### bash

```bash
docker compose run --rm etl pytest
```

## JupyterLab

* URL: `http://127.0.0.1:8888`
* Token: value of `JUPYTER_TOKEN` in `.env`

Get the active Jupyter URL/token (use locally; do not paste tokens into chat or git):

### PowerShell / bash

```bash
docker exec -it pde_jupyter_lab jupyter server list
```

## Logs

Tail Jupyter logs:

```bash
docker logs pde_jupyter_lab --tail 100
```

Tail Postgres logs:

```bash
docker logs pde_postgres_15 --tail 100
```

## Clean rebuild (when dependencies change)

```bash
# Teaching Note: If you mess up the database schema and want to start COMPLETELY fresh, add `-v` to the down command (e.g., `docker compose down -v`). This destroys the persistent Postgres volume.
docker compose down
docker compose build --no-cache
docker compose up -d
```