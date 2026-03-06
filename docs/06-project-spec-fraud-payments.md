# Project Spec — Fraud-Ready Payments Intake (API + CSV)

## Summary
This project ingests financial payment transactions from two sources (API + CSV), standardizes them into a single raw contract (`raw_payments`), enforces a strict Great Expectations quality gate (preventing negative amounts or invalid statuses), and loads into Postgres using a staging-first promote pattern (atomic table swap). It is container-first, testable, and CI-ready.

## Business Context (Use Case)
A platform data engineering team supports multiple payment gateways sending transactional data:
- Partner A delivers processed payments via an API (JSON array).
- Partner B delivers processed payments via a daily CSV file drop.

Downstream consumers rely on a stable raw table with a predictable schema and basic correctness guarantees. The pipeline must fail fast when data is invalid.

## Goals
- Ingest data from both payment gateways as first-class sources.
- Standardize into a single strict raw schema: `raw_payments`.
- Fail the pipeline if quality checks fail (strict gate).
- Load via staging-first promote (atomic swap) to minimize partial states.
- Provide unit tests and artifacts suitable for CI.

## Non-Goals (for this lab)
- Full orchestration (Airflow/Cloud Scheduler).
- Curated layer modeling (dim/fact, marts).
- CDC/streaming ingestion.

---

## Sources

### Partner A — API (JSON)
- Partner identifier: `PARTNER_API_ID` (default: `partner_api`)
- Config: `API_URL`
- Supported:
  - `https://...` (live endpoint via `requests.Session`)
  - `file://...` (local JSON mock via `json.load`)

**Expected payload**: JSON array (list of objects).
Example record:
```json
{
  "txnId": "TXN-30001",
  "accountId": "ACCT-9001",
  "amount": 49.95,
  "currency": "USD",
  "status": "AUTHORIZED",
  "txnTs": "2026-03-01T12:34:56Z"
}
```

### Partner B — CSV file drop

* Partner identifier: `PARTNER_CSV_ID` (default: `partner_csv`)
* Config: `CSV_PATH` (relative path recommended)
* Example CSV header:

```csv
txn_id,account_id,amount,currency,status,txn_ts
C-20001,ACCT-8001,20.00,USD,AUTHORIZED,2026-03-01T10:00:00Z
```

---

## Configuration (Environment Variables)

### Required

* `INGEST_SOURCE` = `api` | `csv` | `both`
* `API_URL` = API endpoint or `file://` path to local JSON mock
* `CSV_PATH` = path to CSV file (relative path recommended)

### Partner IDs

* `PARTNER_API_ID` = `partner_api`
* `PARTNER_CSV_ID` = `partner_csv`

### Database (from `.env`)

* `POSTGRES_USER`
* `POSTGRES_PASSWORD`
* `POSTGRES_DB`
* `DATABASE_HOST` (in Compose network: `postgres`)
* `DATABASE_PORT` (default `5432`)

---

## Standardized Raw Contract

### Target Table: `raw_payments`

Columns:

* `partner_id` (string)
* `txn_id` (string)
* `account_id` (string)
* `amount` (numeric/decimal)  *(Ensures strict financial precision)*
* `currency` (string)
* `status` (string)
* `txn_ts` (datetime)
* `ingested_at` (datetime UTC)

### Semantics

* All sources must map into this schema.
* `ingested_at` is generated upstream during standardization in `src/transform_payments.py` (UTC).

### Uniqueness

* Compound key uniqueness: `(partner_id, txn_id)` must be unique.

---

## Quality Gate (Great Expectations)

### Gate behavior

* Strict fail-fast: if expectations fail, pipeline exits non-zero.
* Artifact is written to `logs/` as JSON for audit/debug (gitignored; uploaded in CI).

### Expectations (minimum contract)

* Required columns exist
* Required fields not null:

  * `partner_id`, `txn_id`, `account_id`, `amount`, `currency`, `status`, `txn_ts`, `ingested_at`
* Validity:

  * `amount >= 0`
  * `currency` matches regex `^[A-Z]{3}$`
  * `status` in allowed set:

    * `AUTHORIZED`, `CAPTURED`, `REFUNDED`, `DECLINED`
* Uniqueness:

  * `(partner_id, txn_id)` unique
* Source-agnostic presence:

  * row count > 0

---

## Loading Strategy (Staging-first Promote)

### Goal

Minimize partial data states and support high-availability reads.

### Strategy

1. Load standardized dataframe into `raw_payments_stg`.
2. Promote to `raw_payments` using an atomic Postgres UPSERT query: `INSERT ... ON CONFLICT (partner_id, txn_id) DO UPDATE ...`

### Transaction Notes

* Uses `engine.begin()` to wrap promote operations in a transaction.
* Includes a degraded path for SQLite to keep unit tests fast and deterministic.

---

## Testing Strategy (pytest)

### Unit tests cover:

* Extract:

  * API JSON mock via `file://` path
  * CSV load via `pandas.read_csv`
* Transform:

  * schema mapping and type enforcement
  * `ingested_at` is present and UTC-like
* Gate:

  * valid dataset passes
  * invalid currency/status fails
  * duplicate `(partner_id, txn_id)` fails
* Load:

  * SQLite in-memory load row count (using generic degraded payload insert since SQLite lacks `ON CONFLICT DO UPDATE` dialect syntax).
  * promote logic exercised where applicable

### Run

```bash
docker compose run --rm etl pytest
```

---

## Acceptance Criteria

* `INGEST_SOURCE=api` loads API payments into `raw_payments` and passes GE.
* `INGEST_SOURCE=csv` loads CSV payments into `raw_payments` and passes GE.
* `INGEST_SOURCE=both` loads both datasets into `raw_payments` and passes GE.
* Any GE failure causes non-zero exit and produces an artifact in `logs/`.
* `pytest` passes in-container with clean output.

---

## Next Milestones (optional)

* Upgrade the SQLite tests to spin up an ephemeral Postgres container in `pytest` natively (via `Testcontainers`).
* Add Airflow/Dagster orchestration around the container execution.
* Add curated table (`curated_payments_daily`) aggregating volumes for analytics use.
