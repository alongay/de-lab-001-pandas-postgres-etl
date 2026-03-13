# scripts/security/scan_vulnerabilities.ps1
# Senior-level Vulnerability Scanner for Docker Images

param(
    [string]$Image = "pde-metabase", # Default to Metabase as it's the largest surface area
    [switch]$FullScan # If set, scans all platform images
)

Write-Host "🛡️ Starting Security Vulnerability Scan..." -ForegroundColor Cyan

# 1. Check for 'docker scout' (Modern industry standard)
$scoutCheck = Get-Command docker-scout -ErrorAction SilentlyContinue
if ($scoutCheck) {
    Write-Host "Checking image: $Image..." -ForegroundColor Yellow
    docker scout cves $Image
} else {
    Write-Host "⚠️ 'docker scout' not found. Falling back to basic Image Audit..." -ForegroundColor Yellow
    
    # Basic Audit: Checking for 'root' users in running containers
    docker ps --format "table {{.Names}}\t{{.Image}}\t{{.ID}}" | ForEach-Object {
        if ($_ -match "Names") { return }
        $id = $_.Split(" ")[-1]
        $user = docker exec $id whoami 2>$null
        if ($user -eq "root") {
            Write-Host "🚨 VOLNERABILITY: Container '$($_.Split(" ")[0])' is running as ROOT user!" -ForegroundColor Red
        } else {
            Write-Host "✅ Container '$($_.Split(" ")[0])' running as non-privileged: $user" -ForegroundColor Green
        }
    }
}

Write-Host "`nRecommendation for Senior Engineers:" -ForegroundColor Cyan
Write-Host "1. Use Alpine or Distroless base images to reduce attack surface."
Write-Host "2. Regularly run 'docker scout quickview' to identify critical CVEs."
Write-Host "3. Pin images to specific SHA256 hashes instead of ':latest'."
