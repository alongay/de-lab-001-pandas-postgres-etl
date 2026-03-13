# 🧹 Maintenance & Operations Matrix

This document defines the "Day 2" routines required to keep the Data Engineering Platform stable, secure, and cost-effective.

## 📊 Maintenance Schudule

| Situation | Required Action | Frequency | Script |
| :--- | :--- | :--- | :--- |
| **PR Preview Deploys** | Cleanup orphaned Cloud Run services | On PR Merge/Close | `scripts/cleanup/cleanup_pr_cloudrun.sh` |
| **Storage Hygiene** | Wipe temporary ingestion data | Weekly | `task.ps1 clean` |
| **Data Quality Drift** | Audit Quarantine growth vs Production | Daily | `scripts/health/check_endpoints.ps1` |
| **Cost Management** | Audit for non-free-tier resources | Monthly | `scripts/cost/list_paid_resources.sh` |
| **Security Posture** | Scan for leaked secrets (pre-commit) | Per Commit | `scripts/security/scan_secrets.ps1` |
| **Documentation** | Verify all demos have valid walkthroughs | Weekly | `scripts/docs/verify_docs_present.ps1` |

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
