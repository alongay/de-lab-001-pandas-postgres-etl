# scripts/health/check_endpoints.ps1
# Validates health of all platform endpoints

$endpoints = @(
    @{ Name = "Airflow"; Url = "http://localhost:8088/health" },
    @{ Name = "Metabase"; Url = "http://localhost:3010/api/health" },
    @{ Name = "Jupyter"; Url = "http://localhost:8888" }
)

foreach ($ep in $endpoints) {
    try {
        $status = Invoke-WebRequest -Uri $ep.Url -Method Get -TimeoutSec 2
        Write-Host "✅ $($ep.Name) is UP ($($status.StatusCode))" -ForegroundColor Green
    } catch {
        Write-Host "❌ $($ep.Name) is DOWN!" -ForegroundColor Red
    }
}
