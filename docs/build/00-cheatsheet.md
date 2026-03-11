# Cheat Sheet — de-lab-001-pandas-postgres-etl

## 🏗️ Start / Stop
### PowerShell
```powershell
# Why: Compiles the custom Python Dockerfile and starts PostgreSQL/Jupyter in the background.
docker compose up -d --build

# Why: Verifies that pde_postgres_15 is (healthy) before running pipelines.
docker compose ps

# Why: Stops and cleanly destroys all active containers.
docker compose down
```

### Bash

```bash
# Why: Compiles the custom Python Dockerfile and starts PostgreSQL/Jupyter in the background.
docker compose up -d --build

# Why: Verifies that pde_postgres_15 is (healthy) before running pipelines.
docker compose ps

# Why: Stops and cleanly destroys all active containers.
docker compose down
```

---

## 🚀 Run ETL

The ETL pipeline evaluates the `INGEST_SOURCE` environment variable to determine which domain to ingest.

### PowerShell

```powershell
# Run Payments ETL
$env:INGEST_SOURCE="both"; docker compose run --rm etl python -m src.payments.etl_run_payments

# Run IoT Batch ETL
docker compose run --rm -e PYTHONPATH=/app etl python -m src.iot.etl_run_iot
```

### Bash

```bash
# Run Payments ETL
INGEST_SOURCE=both docker compose run --rm etl python -m src.payments.etl_run_payments

# Run IoT Batch ETL
INGEST_SOURCE=both docker compose run --rm -e PYTHONPATH=/app etl python -m src.iot.etl_run_iot
```

---

## 🧪 Run Tests

### PowerShell
```powershell
docker compose run --rm etl pytest
```

### Bash
```bash
docker compose run --rm etl pytest
```

---

## 🏎️ Enterprise Streaming (Demo 3)

### Start Infrastructure
```powershell
# Starts Kafka and Spark Cluster
docker compose -f docker-compose.yml -f docker-compose.streaming.yml up -d iot-kafka iot-spark-master iot-spark-worker
```

### Launch Producer & Medallion Streams
```powershell
# Starts Ingestion and Medallion (Bronze/Silver) jobs
docker compose -f docker-compose.yml -f docker-compose.streaming.yml up -d iot-stream-producer iot-bronze-stream iot-silver-stream
```

### Monitor Streaming Logs
```powershell
# Check Producer flow
docker compose -f docker-compose.streaming.yml logs iot-stream-producer -f

# Check Spark execution
docker compose -f docker-compose.streaming.yml logs iot-silver-stream -f
```

---

## 📓 JupyterLab

- **URL**: `http://127.0.0.1:8888`
- **Token**: Value of `JUPYTER_TOKEN` in `.env`

> [!TIP]
> Get the active Jupyter URL/token:
> `docker exec -it pde_jupyter_lab jupyter server list`

---

## 🧹 Clean Rebuild

```bash
# To start COMPLETELY fresh (destroys the persistent volumes):
docker compose down -v
docker compose -f docker-compose.streaming.yml down -v
docker compose build --no-cache
```

---

## 📜 Logs

**Tail Jupyter logs**:
```bash
docker logs pde_jupyter_lab --tail 100
```

**Tail Postgres logs**:
```bash
docker logs pde_postgres_15 --tail 100
```

---

## 🧹 Clean Rebuild

```bash
# To start COMPLETELY fresh (destroys the persistent Postgres volume):
docker compose down -v
docker compose build --no-cache
docker compose up -d
```