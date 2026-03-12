# Cheat Sheet — de-lab-001-pandas-postgres-etl

## 🏗️ Start / Stop
### PowerShell
```powershell
# Why: Starts the Jupyter development environment.
.\task.ps1 up

# Why: Verifies that core services are healthy.
.\task.ps1 ps

# Why: Stops and cleans up active containers.
.\task.ps1 down
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

## 🚀 Run Demo Pipelines

### PowerShell
```powershell
# Run Payments Demo (Isolated on Port 5433)
.\task.ps1 demo-payments

# Run IoT Batch Demo (Isolated on Port 5434)
.\task.ps1 demo-iot

# Run HR Compliance Demo (Isolated on Port 5435)
.\task.ps1 demo-hr
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

## 🏎️ Enterprise Streaming (Demo 5)

### Start Infrastructure
```powershell
# Starts Kafka and Spark Cluster (Isolated)
.\task.ps1 demo-iot-stream
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