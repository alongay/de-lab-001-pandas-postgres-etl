$latest = Get-ChildItem .\logs\ge_validation_*.json | Sort-Object LastWriteTime -Descending | Select-Object -First 1
(Get-Content $latest.FullName | ConvertFrom-Json).results |
Where-Object { $_.success -eq $false } |
Select-Object -First 5 |
Format-List
