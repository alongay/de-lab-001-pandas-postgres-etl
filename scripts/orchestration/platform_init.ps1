Write-Host "`n=== Initializing Orchestration Platform (Idempotent) ===" -ForegroundColor Green

$env_file = ".env"
if (-not (Test-Path $env_file)) {
    Write-Error "Missing .env file. Please run setup first."
    exit 1
}

# Ensure shared network exists
$network_name = "pde_platform_net"
$check_net = docker network ls --filter name=$network_name -q
if (-not $check_net) {
    Write-Host "Creating platform network: $network_name..." -ForegroundColor Cyan
    docker network create $network_name
} else {
    Write-Host "Platform network '$network_name' already exists." -ForegroundColor Gray
}

# Run Airflow Init
Write-Host "Running Airflow Migrations..." -ForegroundColor Cyan
docker compose -f docker-compose.orchestration.yml run --rm airflow-init

Write-Host "`nPlatform Initialization Complete.`n" -ForegroundColor Green
