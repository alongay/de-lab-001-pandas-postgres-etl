# Quality Gates & Testing: Fraud-Ready Payments ETL

This document explains the two primary safety mechanisms built into the `de-lab-001-pandas-postgres-etl` repository: our runtime **Great Expectations** data quality gate, and our **pytest** unit test suite.

---

## 1. The Great Expectations (GE) Quality Gate

**What it is:** A deeply strict, rules-based engine placed precisely between our Extraction logic and our Database loading logic. 

**Why we do this:** In the real world, upstream partners (API or CSV) inevitably send mangled data. A missing `order_total`, a negative refund amount recorded as a positive float, or a non-ISO standard currency (like `US Dollars` instead of `USD`) will poison analytics dashboards and cause downstream machine learning models to fail. The GE gate guarantees that unless the data is structurally immaculate, it will never touch the warehouse.

*   **Execution Location:** Inside domain-specific runners (e.g., `src/payments/etl_run_payments.py`), strictly invoked after the transformation modules and before the Postgres UPSERT/Load scripts.
*   **The Golden Rules Checklist:**
    1.  **Immaculate Schema:** Does the dataframe match the exact column order expected? (`partner_id`, `txn_id`, `account_id`, `status`, `amount`, `currency`, etc.)
    2.  **Zero Null Tolerance:** Are core IDs and totals present? (All core fields including `account_id`, `amount`, and `status` are strictly required).
    3.  **Financial Mathematics:** Is `amount >= 0`? (This blocks refunds recorded as negative floating points).
    4.  **ISO Currency Standards:** Does the `currency` strictly conform to the regex `^[A-Z]{3}$`?
    5.  **State Machine:** Does `status` belong exclusively to the predefined enums `AUTHORIZED`, `CAPTURED`, `REFUNDED`, `DECLINED`?
    6.  **Idempotency Constraint:** Is the `(partner_id, txn_id)` combination mathematically unique?

### Auditing Artifacts
If the GE gate detects even a single row violating these strict contracts, the script crashes non-zero instantly.
**What happens next:** GE programmatically generates a raw JSON audit artifact in `logs/` detailing precisely what rule broke, and exactly which rows failed the regex/null checks. In a CI environment, these artifacts are uploaded as job assets.

---

## 2. The `pytest` Unit Test Suite

**What it is:** A suite of isolated software tests ensuring our core python ETL parsing logic behaves identically across deployments.

**Why we do this:** Before we let our ingestion scripts near a live enterprise environment, we mock the inbound payload and test the schema manipulation locally. We need to mathematically guarantee that our code works. 

### What is Explicitly Tested
1.  **Dual Schema Casting:** The tests mock a raw API record and a raw CSV record independently. They prove that `src/transform_payments.py` casts the string timestamp correctly, transforms the crude floats into strict `decimal.Decimal` components, and generates identical MD5 `record_hash` strings mathematically.
2.  **Valid Data Flow:** We feed perfect mocked datasets into the pipeline and asset the GE quality gate returns a `True` completion. We also perform "Chaos Engineering" in the unit tests by injecting duplicate `txn_id` records to ensure the gate blocks them.
3.  **Atomic Postgres Schema Building:** We feed mock datasets into our `load_payments.py` module. 

### Architectural Fallback (SQLite Testing)
**How we load test without breaking local networking:** During `pytest` runs, we point our loading module to a lightweight, ephemeral SQLite engine loaded into pure computer RAM: `sqlite+pysqlite:///:memory:`. 
Because PostgreSQL's atomic UPSERT (`ON CONFLICT DO UPDATE`) commands are dialectically distinct, our `load_payments.py` script gracefully degrades to generic raw load testing to keep our unit tests blazing fast without relying on actual Docker orchestration availability!

### Running the Suite:
```powershell
.\task.ps1 test
```
When running these tests, any generic warnings triggered by upstream Great Expectations packaging are cleanly suppressed via rules found in `pytest.ini`.
