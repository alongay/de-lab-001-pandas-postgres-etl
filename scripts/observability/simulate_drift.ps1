# simulate_drift.ps1
# Shifts transaction amount distribution to 950.00 to trigger KS-test drift

Write-Host "🚧 Simulating Statistical Drift (Amount Shift to 950.00)..." -ForegroundColor Yellow

$csv_path = "data/payments/transactions_daily.csv"
if (-Not (Test-Path $csv_path)) {
    Write-Error "Payments data not found at $csv_path"
    exit 1
}

$rows = 1..100 | ForEach-Object {
    "TXN-$_,ACCT-$_,950.00,USD,CAPTURED,2026-03-01T12:00:00Z"
}

"txn_id,account_id,amount,currency,status,txn_ts", $rows | Out-File -FilePath $csv_path -Encoding utf8

Write-Host "✅ Drift simulated in $csv_path" -ForegroundColor Green
