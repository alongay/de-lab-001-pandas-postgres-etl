$ErrorActionPreference = "Stop"
$scriptDir = Split-Path $MyInvocation.MyCommand.Path
$scriptsDir = Split-Path $scriptDir
$repoDir = Split-Path $scriptsDir
$paymentsDir = Join-Path $repoDir "data\payments"

if (-not (Test-Path $paymentsDir)) {
    New-Item -ItemType Directory -Force -Path $paymentsDir | Out-Null
}

$csvPath = Join-Path $paymentsDir "transactions_daily.csv"

Write-Host "Injecting CHAOS (High Amount Drift) at $csvPath..."
# We keep the same schema, but multiply the amounts by 100x.
# This will pass Great Expectations (it's still a number) but trigger the KS-test in Observability.
$csvContent = @"
txn_id,account_id,amount,currency,status,txn_ts
TXN-66601,ACCT-9001,4995.00,USD,CAPTURED,$(Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
TXN-66602,ACCT-9002,1500.00,USD,CAPTURED,$(Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
TXN-66603,ACCT-9003,7550.00,USD,DECLINED,$(Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
"@
$csvContent | Out-File -FilePath $csvPath -Encoding utf8

Write-Host "Chaos injected! Statistical Drift is ready for detection."
