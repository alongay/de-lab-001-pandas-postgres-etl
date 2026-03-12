# create_hr_demo_data.ps1
# Generates HR applicant data with PII and compliance edge cases.

$TargetDir = "data/hr/inbound"
if (-not (Test-Path $TargetDir)) { New-Item -ItemType Directory -Force -Path $TargetDir }

$BatchID = Get-Date -Format "yyyyMMdd_HHmm"
$FilePath = "$TargetDir/applicants_$BatchID.csv"

$Data = @(
    "full_name,email,iso_country,role"
    "Alice Smith,alice.smith@example.com,USA,Data Engineer"
    "Bob Jones,bob.jones@corporate.de,DEU,Senior Analyst"
    "Charlie Brown,charlie.pii@leaked.com,GBR,Project Manager"
    "Eve Hacker,eve@malformed@com,FRA,Security Engineer"  # Malformed Email
    "Zhong Li,zhong.li@global.cn,CHN,Director"           # Non-compliant Country (for this demo list)
    "Sarah Connor,sarah.c@tech.sg,SGP,DevOps"
)

$Data | Out-File -FilePath $FilePath -Encoding utf8
Write-Host "Generated HR Applicant Batch: $FilePath" -ForegroundColor Green
