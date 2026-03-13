# 🧹 Maintenance & Operations Matrix

This document defines the "Day 2" routines required to keep the Data Engineering Platform stable, secure, and cost-effective.

## 📊 Maintenance Schedule

| Situation | Required Action | Frequency | Script | Technical Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **PR Preview Deploys** | Cleanup orphaned Cloud Run services | On PR Merge | `scripts/cleanup/cleanup_pr_cloudrun.sh` | **Cost & Security**: Prevents expensive "shadow infrastructure" from persisting after code is merged. |
| **Storage Hygiene** | Wipe temporary ingestion data | Weekly | `task.ps1 clean` | **Deterministic SOT**: Ensures no stale local CSVs/Parquet files interfere with the next idempotent test run. |
| **Data Quality Drift** | Audit Quarantine growth vs Prod | Daily | `scripts/health/check_endpoints.ps1` | **Reliability**: If quarantine is growing faster than prod, your source schema has likely drifted upstream. |
| **Cost Management** | Audit for non-free-tier resources | Monthly | `scripts/cost/list_paid_resources.sh` | **Budget Enforcement**: Prevents surprise "bill shock" from non-preemptible or larger instance classes. |
| **Security Posture** | Scan for leaked secrets | Per Commit | `scripts/security/scan_secrets.ps1` | **Compliance**: Zero-trust pre-flight check to ensure secrets never touch the remote repository logs. |
| **Vulnerability Mgmt** | Scan Docker images for CVEs | Bi-Weekly | `scripts/security/scan_vulnerabilities.ps1` | **Hardening**: Systematically checks for OS-level vulnerabilities (CVEs) and privileged 'root' container risks. |
| **Documentation** | Verify walkthroughs exist | Weekly | `scripts/docs/verify_docs_present.ps1` | **Knowledge Transfer**: Ensures the "Living Lab" remains repeatable for new team members. |

---

## 💰 Cost Model
**Assume $0 Budget Ceiling by Default.**

- **Build Cost**: $0 (GitHub Actions Free Tier / Local Docker)
- **Monthly Ops Cost**: $0 (Local execution)
- **Cost per 1,000 users/month**: $0
- **Note**: If deploying to Cloud Run, **PAY-AS-YOU-GO REQUIRED**. Always check `scripts/cost/list_paid_resources.sh` before leaving.

---

## 🛡️ Security Note
- **Least Privilege**: All database users (`de_user`) have isolated permissions to their specific schemas.
- **Fail-Safe**: If the Quality Gate fails, data is quarantined; it never "fails open" to production.
- **Logs**: PII is redacted automatically in the HR Pipeline logs.

## 🏗️ Rollback Plan
1.  **Code**: Revert to previous Git tag.
2.  **Data**: Delta Lake **Time Travel**. Use `VERSION AS OF` or `TIMESTAMP AS OF` in the streaming layer to restore table state.
3.  **Infrastructure**: `docker compose down` followed by `task.ps1 up`.

---

**Status: PRODUCTION-READY** 🚀🏙️💎🏁
