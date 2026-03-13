# scripts/security/scan_secrets.ps1
# Idempotent secret scanner for pre-commit hooks

$targets = Get-ChildItem -Recurse -File -Exclude ".git", "*.png", "*.webp", ".ipynb"

Write-Host "Scanning for hardcoded secrets..." -ForegroundColor Cyan

$patterns = @(
    "AI_KEY",
    "PASSWORD=",
    "SECRET_KEY",
    "PRIVATE_KEY"
)

foreach ($file in $targets) {
    foreach ($pattern in $patterns) {
        $found_secrets = Select-String -Path $file.FullName -Pattern $pattern
        if ($found_secrets) {
            Write-Host "POTENTIAL SECRET DETECTED in $($file.Name): $pattern" -ForegroundColor Red
        }
    }
}

Write-Host "Security scan finished." -ForegroundColor Green
