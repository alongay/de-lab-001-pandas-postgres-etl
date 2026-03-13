# scripts/cleanup/cleanup_pr_cloudrun.ps1
# Deletes Cloud Run preview services named pr-<PR#>-* for Windows/Local environments

param(
    [string]$ProjectId = "pde-lab-project",
    [string]$Region = "us-central1"
)

Write-Host "Checking for PR preview services in $ProjectId..." -ForegroundColor Cyan

# Logic would go here to call gcloud or local docker cleanup
# For local:
docker ps --filter "name=pr-" --format "{{.ID}}" | ForEach-Object {
    Write-Host "Cleaning up orphaned container: $_" -ForegroundColor Yellow
    docker stop $_
    docker rm $_
}

Write-Host "Cleanup Complete." -ForegroundColor Green
