param(
  [Parameter(Mandatory = $true)]
  [ValidateSet("up", "down", "ps", "logs", "etl", "test", "smoke", "rebuild", "clean", "demo-payments", "demo-iot", "demo-iot-stream")]
  [string]$Task
)

$ErrorActionPreference = "Stop"

function Assert-Docker {
  docker version | Out-Null
  docker compose version | Out-Null
}

function Assert-EnvFile {
  if (-not (Test-Path ".\.env")) {
    Write-Host "Missing .env. Create it from .env.example:" -ForegroundColor Yellow
    Write-Host "  Copy-Item .env.example .env" -ForegroundColor Yellow
    exit 1
  }
}

Assert-Docker

switch ($Task) {
  "up" {
    Assert-EnvFile
    docker compose up -d --build
    docker compose ps
  }
  "down" {
    docker compose down
    docker compose -f docker-compose.streaming.yml down 2>$null
  }
  "ps" {
    docker compose ps
  }
  "logs" {
    docker compose logs -f --tail 200
  }
  "etl" {
    Assert-EnvFile
    $domain = if ($env:DOMAIN) { $env:DOMAIN } else { "payments" }
    docker compose run --rm -e PYTHONPATH=/app etl python -m src.$domain.etl_run_$domain
  }
  "test" {
    docker compose run --rm -e PYTHONPATH=/app etl pytest
  }
  "smoke" {
    Assert-EnvFile
    docker compose up -d --build postgres
    docker compose run --rm etl python -m src.payments.etl_run_payments
    docker compose down
  }
  "rebuild" {
    Assert-EnvFile
    docker compose down
    docker compose build --no-cache
    docker compose up -d
    docker compose ps
  }
  "clean" {
    # Destructive: removes volumes (DB data)
    docker compose down -v
    docker compose -f docker-compose.streaming.yml down -v 2>$null
  }
  "demo-payments" {
    Assert-EnvFile
    Write-Host "`n=== 1. Starting Services ===" -ForegroundColor Green
    docker compose up -d --build
    
    Write-Host "`n=== 2. Generating Demo Data ===" -ForegroundColor Green
    .\scripts\payments\create_payments_demo_data.ps1

    Write-Host "`n=== 3. Initializing / Resetting Database State ===" -ForegroundColor Green
    Start-Sleep -Seconds 3
    docker compose run --rm -e PYTHONPATH=/app etl python -m scripts.payments.init_payments_db
    docker exec pde_postgres_15 sh -lc "psql -P pager=off -U `$POSTGRES_USER -d `$POSTGRES_DB -c 'TRUNCATE TABLE raw_payments;'"
    if ($LASTEXITCODE -ne 0) {
      docker exec pde_postgres_15 sh -lc "psql -P pager=off -U de_user -d de_workshop -c 'TRUNCATE TABLE raw_payments;'"
    }

    Write-Host "`n=== 4. Running Happy Path (both sources) ===" -ForegroundColor Green
    $env:INGEST_SOURCE = "both"
    docker compose run --rm etl python -m src.payments.etl_run_payments

    Write-Host "`n=== 5. Injecting Chaos (Negative Amount) ===" -ForegroundColor Green
    $chaosCsv = @"
txn_id,account_id,amount,currency,status,txn_ts
TXN-30001,ACCT-9001,49.95,USD,CAPTURED,2026-03-01T12:34:56Z
TXN-30002,ACCT-9002,-75.50,USD,CAPTURED,2026-03-01T12:35:56Z
TXN-30003,ACCT-9003,75.50,USD,DECLINED,2026-03-01T12:36:56Z
"@
    $chaosCsv | Out-File -FilePath .\data\payments\transactions_daily.csv -Encoding utf8

    Write-Host "`n=== 6. Expected Failure (Great Expectations catches bad data) ===" -ForegroundColor Yellow
    $env:INGEST_SOURCE = "csv"
    docker compose run --rm etl python -m src.payments.etl_run_payments
    Write-Host "Look in logs/ for the generated GE artifact detailing the failure.`n" -ForegroundColor Yellow

    Write-Host "`n=== 7. Proving Recovery (Fixing CSV) ===" -ForegroundColor Green
    .\scripts\payments\create_payments_demo_data.ps1 | Out-Null
    docker compose run --rm etl python -m src.payments.etl_run_payments

    Write-Host "`n=== 8. Archiving Chaos Artifact ===" -ForegroundColor Green
    if (-not (Test-Path ".\artifacts")) { New-Item -ItemType Directory -Force -Path ".\artifacts" | Out-Null }
    $latest = Get-ChildItem .\logs\ge_validation_*.json | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    if ($latest) {
      Copy-Item $latest.FullName -Destination ".\artifacts\latest_chaos_failure.json"
      Write-Host "Copied GE failure log to artifacts/latest_chaos_failure.json" -ForegroundColor Green
    }

    Write-Host "`n=== 9. Tearing down services ===" -ForegroundColor Green
    docker compose down
    Write-Host "`nDemo run complete!" -ForegroundColor Green
  }
  "demo-iot" {
    Assert-EnvFile
    Write-Host "`n=== 1. Starting Services (IoT Mode) ===" -ForegroundColor Green
    docker compose up -d --build
    
    Write-Host "`n=== 2. Resetting Database (IoT Tables) ===" -ForegroundColor Green
    # Wait for postgres
    Start-Sleep -Seconds 3
    docker exec pde_postgres_15 sh -lc "psql -P pager=off -U `$POSTGRES_USER -d `$POSTGRES_DB -c 'TRUNCATE TABLE raw_sensor_readings, raw_sensor_readings_quarantine CASCADE;'"
    if ($LASTEXITCODE -ne 0) {
      docker exec pde_postgres_15 sh -lc "psql -P pager=off -U de_user -d de_workshop -c 'TRUNCATE TABLE raw_sensor_readings, raw_sensor_readings_quarantine CASCADE;'"
    }

    Write-Host "`n=== 3. Running Happy Path (Low Outliers) ===" -ForegroundColor Green
    .\scripts\iot\create_iot_demo_data.ps1 -DeviceCount 10 -Minutes 30 -OutlierRate 0.0 -MissingTsRate 0.0
    docker compose run --rm -e PYTHONPATH=/app etl python -m src.iot.etl_run_iot
    
    Write-Host "`n=== 4. Injecting Chaos (High Outliers) ===" -ForegroundColor Green
    .\scripts\iot\create_iot_demo_data.ps1 -DeviceCount 10 -Minutes 30 -OutlierRate 0.8 -MissingTsRate 0.0
    docker compose run --rm -e PYTHONPATH=/app etl python -m src.iot.etl_run_iot
    Write-Host "Expected exit code 1 due to the Quarantine Pattern." -ForegroundColor Yellow

    Write-Host "`n=== 5. Verifying Data Partitioning ===" -ForegroundColor Green
    docker exec pde_postgres_15 sh -lc "psql -P pager=off -U de_user -d de_workshop -c 'SELECT metric, COUNT(*) FROM raw_sensor_readings GROUP BY metric;'"
    Write-Host "--- Quarantine Table ---" -ForegroundColor Yellow
    docker exec pde_postgres_15 sh -lc "psql -P pager=off -U de_user -d de_workshop -c 'SELECT metric, COUNT(*) FROM raw_sensor_readings_quarantine GROUP BY metric;'"
    
    Write-Host "`n=== 6. Verifying Partitioning (Senior DE Check) ===" -ForegroundColor Green
    docker exec pde_postgres_15 sh -lc "psql -P pager=off -U de_user -d de_workshop -c 'SELECT relname as partition_name, n_live_tup as row_count FROM pg_stat_user_tables WHERE relname LIKE ''raw_sensor_readings_y%'';'"

    Write-Host "`n=== 6. Tearing down services ===" -ForegroundColor Green
    docker compose down
    Write-Host "`nIoT Demo complete!" -ForegroundColor Green
  }
  "demo-iot-stream" {
    Assert-EnvFile
    Write-Host "`n=== 1. Starting Infrastructure (Option A: Separate Compose) ===" -ForegroundColor Green
    docker compose -f docker-compose.yml -f docker-compose.streaming.yml up -d --build iot-kafka iot-spark-master iot-spark-worker
    
    Write-Host "`n=== 2. Creating Kafka Topics ===" -ForegroundColor Green
    Start-Sleep -Seconds 10
    .\scripts\streaming\create_kafka_topic.ps1

    Write-Host "`n=== 3. Starting Medallion Pipelines (Bronze -> Silver) ===" -ForegroundColor Green
    docker compose -f docker-compose.yml -f docker-compose.streaming.yml up -d iot-bronze-stream iot-silver-stream
    
    Write-Host "`n=== 4. Starting Event Producer (Injecting Chaos) ===" -ForegroundColor Green
    docker compose -f docker-compose.yml -f docker-compose.streaming.yml up -d iot-stream-producer
    
    Write-Host "`n=== 5. Monitoring Pipeline (Waiting for Data) ===" -ForegroundColor Green
    Write-Host "Streaming is live. Observe the Spark jobs at http://localhost:8080" -ForegroundColor Cyan
    Start-Sleep -Seconds 25
    
    Write-Host "`n=== 6. Verifying Data Landing (Medallion Layers) ===" -ForegroundColor Green
    docker exec pde-jupyter-lab ls -R /app/data/iot/delta/bronze
    docker exec pde-jupyter-lab ls -R /app/data/iot/delta/silver
    
    Write-Host "`n=== 7. Chaos Check (Quarantine) ===" -ForegroundColor Green
    Write-Host "Scanning for flagged anomalies in the Quarantine Delta Table..." -ForegroundColor Yellow
    docker exec pde-jupyter-lab python -c "import os; print('Anomalies Detected!' if os.path.exists('/app/data/iot/delta/quarantine') else 'No Anomalies Yet (Waiting...)')"

    Write-Host "`n=== 8. Tearing down streaming platform ===" -ForegroundColor Green
    docker compose -f docker-compose.yml -f docker-compose.streaming.yml down
    Write-Host "`nStreaming Demo complete!" -ForegroundColor Green
  }
}
