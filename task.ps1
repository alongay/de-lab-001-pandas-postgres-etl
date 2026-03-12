param(
  [Parameter(Mandatory = $true)]
  [ValidateSet("up", "down", "ps", "logs", "etl", "test", "smoke", "rebuild", "clean", "demo-payments", "demo-iot", "demo-iot-stream", "demo-orchestration", "demo-hr", "demo-observability", "platform-up", "platform-down", "platform-init", "platform-status")]
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
    $domain = "payments"
    if ($env:DOMAIN) { $domain = $env:DOMAIN }
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
    docker compose down -v
    docker compose -f docker-compose.streaming.yml down -v 2>$null
  }
  "demo-payments" {
    Assert-EnvFile
    Write-Host "`n=== 1. Starting Services (Isolated Payments Mode) ===" -ForegroundColor Green
    docker compose -f docker-compose.payments.yml up -d --build
    
    Write-Host "`n=== 2. Generating Demo Data ===" -ForegroundColor Green
    .\scripts\payments\create_payments_demo_data.ps1

    Write-Host "`n=== 3. Initializing / Resetting Database State ===" -ForegroundColor Green
    Start-Sleep -Seconds 8
    docker compose -f docker-compose.payments.yml run --rm payments-etl python -m scripts.payments.init_payments_db
    docker compose -f docker-compose.payments.yml exec -T payments-postgres sh -lc "psql -P pager=off -U `$POSTGRES_USER -d `$POSTGRES_DB -c 'TRUNCATE TABLE raw_payments;'"
    if ($LASTEXITCODE -ne 0) {
      docker compose -f docker-compose.payments.yml exec -T payments-postgres sh -lc "psql -P pager=off -U de_user -d de_workshop -c 'TRUNCATE TABLE raw_payments;'"
    }

    Write-Host "`n=== 4. Running Happy Path (both sources) ===" -ForegroundColor Green
    $env:INGEST_SOURCE = "both"
    docker compose -f docker-compose.payments.yml run --rm payments-etl python -m src.payments.etl_run_payments

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
    docker compose -f docker-compose.payments.yml run --rm payments-etl python -m src.payments.etl_run_payments
    Write-Host "Look in logs/ for the generated GE artifact detailing the failure.`n" -ForegroundColor Yellow

    Write-Host "`n=== 7. Proving Recovery (Fixing CSV) ===" -ForegroundColor Green
    .\scripts\payments\create_payments_demo_data.ps1 | Out-Null
    docker compose -f docker-compose.payments.yml run --rm payments-etl python -m src.payments.etl_run_payments

    Write-Host "`n=== 8. Archiving Chaos Artifact ===" -ForegroundColor Green
    if (-not (Test-Path ".\artifacts")) { New-Item -ItemType Directory -Force -Path ".\artifacts" | Out-Null }
    $latest = Get-ChildItem .\logs\ge_validation_*.json | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    if ($latest) {
      Copy-Item $latest.FullName -Destination ".\artifacts\latest_chaos_failure.json"
      Write-Host "Copied GE failure log to artifacts/latest_chaos_failure.json" -ForegroundColor Green
    }

    Write-Host "`n=== 9. Tearing down services ===" -ForegroundColor Green
    docker compose -f docker-compose.payments.yml down
    Write-Host "`nDemo run complete!" -ForegroundColor Green
  }
  "demo-iot" {
    Assert-EnvFile
    Write-Host "`n=== 1. Starting Services (Isolated IoT Mode) ===" -ForegroundColor Green
    docker compose -f docker-compose.iot.yml up -d --build
    
    Write-Host "`n=== 2. Resetting Database (IoT Tables) ===" -ForegroundColor Green
    Start-Sleep -Seconds 8
    docker compose -f docker-compose.iot.yml exec -T iot-postgres sh -lc "psql -P pager=off -U `$POSTGRES_USER -d `$POSTGRES_DB -c 'TRUNCATE TABLE raw_sensor_readings, raw_sensor_readings_quarantine CASCADE;'"
    if ($LASTEXITCODE -ne 0) {
      docker compose -f docker-compose.iot.yml exec -T iot-postgres sh -lc "psql -P pager=off -U de_user -d de_workshop -c 'TRUNCATE TABLE raw_sensor_readings, raw_sensor_readings_quarantine CASCADE;'"
    }

    Write-Host "`n=== 3. Running Happy Path (Low Outliers) ===" -ForegroundColor Green
    .\scripts\iot\create_iot_demo_data.ps1 -DeviceCount 10 -Minutes 30 -OutlierRate 0.0 -MissingTsRate 0.0
    docker compose -f docker-compose.iot.yml run --rm -e PYTHONPATH=/app iot-etl python -m src.iot.etl_run_iot
    
    Write-Host "`n=== 4. Injecting Chaos (High Outliers) ===" -ForegroundColor Green
    .\scripts\iot\create_iot_demo_data.ps1 -DeviceCount 10 -Minutes 30 -OutlierRate 0.8 -MissingTsRate 0.0
    docker compose -f docker-compose.iot.yml run --rm -e PYTHONPATH=/app iot-etl python -m src.iot.etl_run_iot
    Write-Host "Expected exit code 1 due to the Quarantine Pattern." -ForegroundColor Yellow

    Write-Host "`n=== 5. Verifying Data Partitioning ===" -ForegroundColor Green
    docker compose -f docker-compose.iot.yml exec -T iot-postgres sh -lc "psql -P pager=off -U `$POSTGRES_USER -d `$POSTGRES_DB -c 'SELECT metric, COUNT(*) FROM raw_sensor_readings GROUP BY metric;'"
    Write-Host "--- Quarantine Table ---" -ForegroundColor Yellow
    docker compose -f docker-compose.iot.yml exec -T iot-postgres sh -lc "psql -P pager=off -U `$POSTGRES_USER -d `$POSTGRES_DB -c 'SELECT metric, COUNT(*) FROM raw_sensor_readings_quarantine GROUP BY metric;'"
    
    Write-Host "`n=== 6. Verifying Partitioning (Senior DE Check) ===" -ForegroundColor Green
    docker compose -f docker-compose.iot.yml exec -T iot-postgres sh -lc "psql -P pager=off -U `$POSTGRES_USER -d `$POSTGRES_DB -c 'SELECT relname as partition_name, n_live_tup as row_count FROM pg_stat_user_tables WHERE relname LIKE ''raw_sensor_readings_y%'';'"

    Write-Host "`n=== 7. Tearing down services ===" -ForegroundColor Green
    docker compose -f docker-compose.iot.yml down
    Write-Host "`nIoT Demo complete!" -ForegroundColor Green
  }
  "demo-iot-stream" {
    Assert-EnvFile
    Write-Host "`n=== 1. Starting Infrastructure ===" -ForegroundColor Green
    docker compose -f docker-compose.yml -f docker-compose.streaming.yml up -d --build iot-kafka iot-spark-master iot-spark-worker
    
    Write-Host "`n=== 2. Creating Kafka Topics ===" -ForegroundColor Green
    Start-Sleep -Seconds 10
    .\scripts\streaming\create_kafka_topic.ps1

    Write-Host "`n=== 3. Starting Medallion Pipelines (Bronze -> Silver) ===" -ForegroundColor Green
    docker compose -f docker-compose.yml -f docker-compose.streaming.yml up -d iot-bronze-stream iot-silver-stream
    
    Write-Host "`n=== 4. Starting Event Producer (Injecting Chaos) ===" -ForegroundColor Green
    docker compose -f docker-compose.yml -f docker-compose.streaming.yml up -d iot-stream-producer
    
    Write-Host "`n=== 5. Monitoring Pipeline (Waiting for Data) ===" -ForegroundColor Green
    Start-Sleep -Seconds 25
    
    Write-Host "`n=== 6. Verifying Data Landing ===" -ForegroundColor Green
    docker compose -f docker-compose.yml -f docker-compose.streaming.yml exec -T jupyter ls -R /app/data/streaming/delta/bronze
    docker compose -f docker-compose.yml -f docker-compose.streaming.yml exec -T jupyter ls -R /app/data/streaming/delta/silver
    
    Write-Host "`n=== 7. Chaos Check (Quarantine) ===" -ForegroundColor Green
    docker compose -f docker-compose.yml -f docker-compose.streaming.yml exec -T jupyter python -c "import os; print('Anomalies Detected!' if os.path.exists('/app/data/streaming/delta/quarantine') else 'No Anomalies Yet...')"

    Write-Host "`n=== 8. Tearing down streaming platform ===" -ForegroundColor Green
    docker compose -f docker-compose.yml -f docker-compose.streaming.yml down
    Write-Host "`nStreaming Demo complete!" -ForegroundColor Green
  }
  "platform-up" {
    Assert-EnvFile
    Write-Host "`n=== 1. Starting Orchestration Platform ===" -ForegroundColor Green
    docker compose -f docker-compose.orchestration.yml up -d
  }
  "platform-down" {
    docker compose -f docker-compose.orchestration.yml down
  }
  "platform-init" {
    powershell -ExecutionPolicy Bypass -File .\scripts\orchestration\platform_init.ps1
  }
  "platform-status" {
    Write-Host "`n=== Platform Health & DAG Integrity ===" -ForegroundColor Green
    docker exec pde-airflow-scheduler airflow dags reserialize
    docker exec pde-airflow-scheduler python /opt/airflow/scripts/orchestration/dag_validator.py
    docker exec pde-airflow-scheduler airflow dags list
  }
  "demo-orchestration" {
    Assert-EnvFile
    Write-Host "`n=== 1. Starting Hybrid Platform ===" -ForegroundColor Green
    docker compose up -d
    docker compose -f docker-compose.streaming.yml up -d
    .\task.ps1 platform-init
    .\task.ps1 platform-up
    Write-Host "`nPlatform is LIVE at http://localhost:8088" -ForegroundColor Cyan
  }
  "demo-hr" {
    Assert-EnvFile
    Write-Host "`n=== 1. Starting Services (Isolated HR Mode) ===" -ForegroundColor Green
    docker compose -f docker-compose.hr.yml up -d --build
    
    Write-Host "`n=== 2. Resetting Database (HR Tables) ===" -ForegroundColor Green
    # The containers are now named pde_hr_postgres and pde_hr_etl_runner
    docker compose -f docker-compose.hr.yml exec -T hr-postgres sh -lc "psql -P pager=off -U `$POSTGRES_USER -d `$POSTGRES_DB -f /app/scripts/hr/init_hr_db.sql"
    docker compose -f docker-compose.hr.yml exec -T hr-postgres sh -lc "psql -P pager=off -U `$POSTGRES_USER -d `$POSTGRES_DB -c 'TRUNCATE TABLE hr_applicants, hr_applicants_quarantine;'"

    Write-Host "`n=== 3. Generating Applicant Data ===" -ForegroundColor Green
    .\scripts\hr\create_hr_demo_data.ps1

    Write-Host "`n=== 4. Running HR ETL Pipeline ===" -ForegroundColor Green
    if (-not (Test-Path ".\logs")) { New-Item -ItemType Directory -Force -Path ".\logs" | Out-Null }
    docker compose -f docker-compose.hr.yml run --rm hr-etl python -m src.hr.etl_run_hr

    Write-Host "`n=== 5. Verifying PII Redaction in Logs ===" -ForegroundColor Green
    if (Test-Path .\logs\etl.log) {
        $logs = Get-Content -Path .\logs\etl.log -Tail 20
        if ($logs -match "\[REDACTED\]") {
          Write-Host "SUCCESS: PII Redaction verified in logs/etl.log" -ForegroundColor Green
        } else {
          Write-Host "WARNING: PII Redaction not detected." -ForegroundColor Yellow
        }
    }

    Write-Host "`n=== 6. Checking Compliance Data (Postgres) ===" -ForegroundColor Green
    docker compose -f docker-compose.hr.yml exec -T hr-postgres sh -lc "psql -P pager=off -U `$POSTGRES_USER -d `$POSTGRES_DB -c 'SELECT full_name, iso_country, role FROM hr_applicants;'"
    Write-Host "--- Quarantined (Compliance Breach) ---" -ForegroundColor Yellow
    docker compose -f docker-compose.hr.yml exec -T hr-postgres sh -lc "psql -P pager=off -U `$POSTGRES_USER -d `$POSTGRES_DB -c 'SELECT full_name, email, failure_reason FROM hr_applicants_quarantine;'"

    Write-Host "`n=== 7. Tearing down services ===" -ForegroundColor Green
    docker compose -f docker-compose.hr.yml down
    Write-Host "`nHR Privacy Demo complete!" -ForegroundColor Green
  }
  "demo-observability" {
    Assert-EnvFile
    Write-Host "`n=== 1. Starting Lab Platform (Pre-requisite) ===" -ForegroundColor Green
    docker compose up -d postgres
    
    Write-Host "`n=== 2. Establishing Happy Path Baseline ===" -ForegroundColor Green
    .\scripts\payments\create_payments_demo_data.ps1
    $env:INGEST_SOURCE = "csv"
    docker compose run --rm -e PYTHONPATH=/app etl python -m src.payments.etl_run_payments
    
    Write-Host "`n=== 3. Simulating Statistical Drift (Amount Shift) ===" -ForegroundColor Green
    .\scripts\observability\simulate_drift.ps1
    docker compose run --rm -e PYTHONPATH=/app etl python -m src.payments.etl_run_payments
    
    Write-Host "`n=== 4. Running Observability Audit (Metadata Lake Hub) ===" -ForegroundColor Green
    docker compose -f docker-compose.observability.yml up observability-hub
    
    Write-Host "`n=== 5. Tearing down demo services ===" -ForegroundColor Green
    docker compose down
    docker compose -f docker-compose.observability.yml down
    Write-Host "`nObservability Demo complete!" -ForegroundColor Green
  }
}
