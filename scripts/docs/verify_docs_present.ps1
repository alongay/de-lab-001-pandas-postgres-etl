# scripts/docs/verify_docs_present.ps1
# Ensures all critical repo documentation exists

$docs = @(
    "README.md",
    "docs/architecture/README.md",
    "docs/operations/05-maintenance-matrix.md",
    "docs/operations/hands-on-mastery-guide.md"
)

foreach ($doc in $docs) {
    if (Test-Path $doc) {
        Write-Host "✅ $doc exists." -ForegroundColor Green
    } else {
        Write-Host "⚠️ MISSING: $doc" -ForegroundColor Red
    }
}
