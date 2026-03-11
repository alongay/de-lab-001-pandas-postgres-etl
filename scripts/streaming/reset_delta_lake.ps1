# reset_delta_lake.ps1
# Wipes the Delta Lake tables and Spark checkpoints for a fresh demo run.

$ErrorActionPreference = "Continue"

Write-Host "🧹 Cleaning Delta Lake Tables..." -ForegroundColor Yellow
if (Test-Path ".\data\delta") {
    Remove-Item -Path ".\data\delta\*" -Recurse -Force
    Write-Host "✅ Delta data wiped." -ForegroundColor Green
}

Write-Host "🧹 Cleaning Spark Checkpoints..." -ForegroundColor Yellow
if (Test-Path ".\_checkpoints") {
    Remove-Item -Path ".\_checkpoints" -Recurse -Force
    Write-Host "✅ Checkpoints wiped." -ForegroundColor Green
}

Write-Host "`nDelta Lake is now in a clean state." -ForegroundColor Cyan
