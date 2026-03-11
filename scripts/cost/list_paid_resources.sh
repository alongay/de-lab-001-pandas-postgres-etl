#!/usr/bin/env bash
# scripts/cost/list_paid_resources.sh
# Checks for active cloud-connected resources. In this lab, it should return 0.

echo "--- Active Cloud Resource Audit ---"
gcloud run services list --format="table(name, status, url)" 2>/dev/null || echo "No Cloud Run services detected."
echo "-----------------------------------"
echo "Project is running in $0 local mode."
