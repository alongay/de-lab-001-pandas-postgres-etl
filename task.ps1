param(
  [Parameter(Mandatory = $true)]
  [ValidateSet("up", "down", "ps", "logs", "etl", "test", "smoke", "rebuild", "clean", "demo-payments")]
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
  }
  "ps" {
    docker compose ps
  }
  "logs" {
    docker compose logs -f --tail 200
  }
  "etl" {
    Assert-EnvFile
    docker compose run --rm etl
  }
  "test" {
    docker compose run --rm etl pytest
  }
  "smoke" {
    Assert-EnvFile
    docker compose up -d --build postgres
    docker compose run --rm etl
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
  }
  "demo-payments" {
    Assert-EnvFile
    Write-Host "`n=== 1. Starting Services ===" -ForegroundColor Green
    docker compose up -d --build
    
    Write-Host "`n=== 2. Generating Demo Data ===" -ForegroundColor Green
    .\scripts\create_payments_demo_data.ps1

    Write-Host "`n=== 3. Resetting Database State ===" -ForegroundColor Green
    # Wait for postgres to be ready
    Start-Sleep -Seconds 3
    docker exec pde_postgres_15 sh -lc "psql -P pager=off -U `$POSTGRES_USER -d `$POSTGRES_DB -c 'TRUNCATE TABLE raw_payments;'"
    if ($LASTEXITCODE -ne 0) {
      docker exec pde_postgres_15 sh -lc "psql -P pager=off -U de_user -d de_workshop -c 'TRUNCATE TABLE raw_payments;'"
    }

    Write-Host "`n=== 4. Running Happy Path (both sources) ===" -ForegroundColor Green
    $env:INGEST_SOURCE = "both"
    docker compose run --rm etl

    Write-Host "`n=== 5. Injecting Chaos (Negative Amount) ===" -ForegroundColor Green
    $chaosCsv = @"
txn_id,account_id,amount,currency,status,txn_ts
TXN-30001,ACCT-9001,49.95,USD,CAPTURED,2026-03-01T12:34:56Z
TXN-30002,ACCT-9002,-75.50,USD,CAPTURED,2026-03-01T12:35:56Z
TXN-30003,ACCT-9003,75.50,USD,DECLINED,2026-03-01T12:36:56Z
"@
    $chaosCsv | Out-File -FilePath .\data\inbound\transactions_daily.csv -Encoding utf8

    Write-Host "`n=== 6. Expected Failure (Great Expectations catches bad data) ===" -ForegroundColor Yellow
    $env:INGEST_SOURCE = "csv"
    docker compose run --rm etl
    Write-Host "Look in logs/ for the generated GE artifact detailing the failure.`n" -ForegroundColor Yellow

    Write-Host "`n=== 7. Proving Recovery (Fixing CSV) ===" -ForegroundColor Green
    .\scripts\create_payments_demo_data.ps1 | Out-Null
    docker compose run --rm etl

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
}
