param(
  [int]$DeviceCount = 25,
  [int]$Minutes = 60,
  [double]$OutlierRate = 0.03,
  [double]$MissingTsRate = 0.01
)

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path $MyInvocation.MyCommand.Path
$scriptsDir = Split-Path $scriptDir
$repoDir = Split-Path $scriptsDir
$inbound = Join-Path $repoDir "data\iot\inbound"
if (-not (Test-Path $inbound)) {
    New-Item -ItemType Directory -Force -Path $inbound | Out-Null
}

function New-ReadingRow {
  param($deviceId, $ts, $metric)

  if ($metric -eq "temp_c") {
    $unit = "c"
    $value = [math]::Round((20 + (Get-Random -Minimum -5 -Maximum 8) + (Get-Random -Minimum 0.0 -Maximum 1.0)), 2)
    # Outliers: unrealistic temps
    if ((Get-Random -Minimum 0.0 -Maximum 1.0) -lt $OutlierRate) { $value = (Get-Random -Minimum -60 -Maximum 120) }
  }
  elseif ($metric -eq "humidity_pct") {
    $unit = "pct"
    $value = [math]::Round((40 + (Get-Random -Minimum -15 -Maximum 25) + (Get-Random -Minimum 0.0 -Maximum 1.0)), 2)
    # Outliers: impossible humidity
    if ((Get-Random -Minimum 0.0 -Maximum 1.0) -lt $OutlierRate) { $value = (Get-Random -Minimum -30 -Maximum 170) }
  }
  elseif ($metric -eq "pressure_hpa") {
    $unit = "hpa"
    $value = [math]::Round((1013 + (Get-Random -Minimum -30 -Maximum 30) + (Get-Random -Minimum 0.0 -Maximum 1.0)), 2)
    # Outliers
    if ((Get-Random -Minimum 0.0 -Maximum 1.0) -lt $OutlierRate) { $value = (Get-Random -Minimum 100 -Maximum 2000) }
  }

  # Unit mismatch chaos
  if ((Get-Random -Minimum 0.0 -Maximum 1.0) -lt ($OutlierRate / 2)) {
    $unit = "F"  # wrong for temp_c
  }

  # Missing timestamp chaos
  $tsOut = $ts
  if ((Get-Random -Minimum 0.0 -Maximum 1.0) -lt $MissingTsRate) { $tsOut = "" }

  return [PSCustomObject]@{
    device_id   = $deviceId
    reading_ts  = $tsOut
    metric      = $metric
    value       = $value
    unit        = $unit
  }
}

$rows = New-Object System.Collections.Generic.List[object]
$start = (Get-Date "2026-03-01T00:00:00Z").ToUniversalTime()

for ($d=1; $d -le $DeviceCount; $d++) {
  $deviceId = ("DEV-{0:0000}" -f $d)
  for ($m=0; $m -lt $Minutes; $m++) {
    $ts = ($start.AddMinutes($m)).ToString("yyyy-MM-ddTHH:mm:ssZ")
    foreach ($metric in @("temp_c","humidity_pct","pressure_hpa")) {
      $rows.Add((New-ReadingRow -deviceId $deviceId -ts $ts -metric $metric))
    }
  }
}

# Write CSV
$csvPath = Join-Path $inbound "telemetry.csv"
$rows | Export-Csv -NoTypeInformation -Path $csvPath

# Write JSON (API mock)
$jsonPath = Join-Path $inbound "telemetry.json"
($rows | ConvertTo-Json -Depth 4) | Out-File -Encoding utf8 $jsonPath

Write-Host "Generated:"
Write-Host "  $csvPath"
Write-Host "  $jsonPath"
Write-Host ("Rows: {0}" -f $rows.Count)
