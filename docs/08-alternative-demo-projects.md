# Curriculum: Educational Demo Projects

This guide outlines three distinct, enterprise-grade data engineering scenarios designed to be taught using this repository's architecture (Docker + Postgres + ETL Modules + Jupyter + GE + Pytest). 

These are designed as "teaching flows." Each project leverages the exact same containerized pipeline pattern but introduces a unique business domain with specific platform challenges: financial transactions, IoT outliers, or PII redaction.

***

## Demo Project 1: Fraud-Ready Payments Intake (✅ Currently Implemented)

**The Pitch:**
This is the default domain currently running in the repository! The audience learns how to handle money (precision casting), strict validation rules (fraud prevention), and how the Great Expectations gate natively traps impossible states before they hit the data warehouse.

### 1. The Domain Requirements
*   **Target Schema (`raw_payments`):** `partner_id` (string), `txn_id` (string), `account_id` (string), `amount` (numeric/float), `currency` (string), `status` (string), `txn_ts` (datetime), `ingested_at` (datetime UTC).
*   **Quality Gate Rules:**
    *   `amount >= 0` (block negative payments/refunds sent as negative amounts).
    *   `currency` must strictly match the regex `^[A-Z]{3}$` (e.g., USD, EUR).
    *   `status` must belong to the strict set: `AUTHORIZED | CAPTURED | REFUNDED | DECLINED`.
    *   `txn_ts` must not reflect a future date (e.g., <= now + 5 minutes).
    *   Compound uniqueness on `(partner_id, txn_id)`.

### 2. The Step-by-Step Teaching Flow

**Step 1 — Prepare the Inbound Files**
*   **What you are doing:** Creating the synthetic partner payloads.
*   **Instruction:** Create `data/inbound/transactions.json` to simulate the live API, and `data/inbound/transactions_daily.csv` to simulate the batch drop. 

**Step 2 — Configure the Environment**
*   **What you are doing:** Routing the ETL to the new data sources.
*   **Instruction:** Open `.env` and set `INGEST_SOURCE=both`. Map `API_URL=file:///app/data/inbound/transactions.json` and `CSV_PATH=data/inbound/transactions_daily.csv`.

**Step 3 — Profile the Raw Data (Jupyter)**
*   **What you are doing:** Showing students how to interactively explore an unknown dataset before writing ETL code.
*   **Instruction:** Open `notebooks/01_explore_payments.ipynb`. Run `.info()`, check for null rates, observe the min/max distributions of `amount`, and isolate duplicate `(partner_id, txn_id)` pairs.

**Step 4 — Execute the Pipeline**
*   **What you are doing:** Running the "Happy Path" ingestion.
*   **Instruction:** Run `docker compose run --rm etl`. Next, connect to Postgres and run a `SELECT COUNT(*)` grouping by `partner_id` to prove the ingestion succeeded.

**Step 5 — The "Chaos Engineering" Test**
*   **What you are doing:** Proving the quality gate is functional and strict.
*   **Instruction:** Go back to your `transactions.json` file and intentionally corrupt a row (e.g., set `amount: -10`). Re-run `docker compose run --rm etl`. You want the audience to see the **non-zero exit** failure. Show them the generated artifact in `logs/` clearly calling out the broken expectation.

**Step 6 — CI Parity Testing**
*   **What you are doing:** Proving that the pipeline is protected against regressions.
*   **Instruction:** Run `docker compose run --rm etl pytest` to exercise the test suite (checking transform logic, schema mapping, and SQLite fallback loading).

***

## Future Exercise 1: IoT Sensor Telemetry Intake (API + CSV)

**The Pitch:**
*This is an exercise for the student to implement by modifying the `src/` modules.*
Shift focus from pure finance to high-volume machine data. This teaches students how to handle outliers, timeseries events, and physical constraints (e.g. impossible temperature readings).

### 1. The Domain Requirements
*   **Target Schema (`raw_sensor_readings`):** `device_id` (string), `reading_ts` (datetime), `metric` (string, e.g., `temp_c`, `humidity_pct`), `value` (float), `unit` (string), `partner_id` (string), `ingested_at` (datetime UTC).
*   **Quality Gate Rules:**
    *   `value` explicitly bounded by the `metric` type (e.g., `humidity_pct` between 0-100).
    *   `unit` perfectly corresponds to `metric` (no `temp_c` labeled with `Fahrenheit`).
    *   Compound uniqueness across the timeseries node: `(partner_id, device_id, reading_ts, metric)`.

### 2. The Step-by-Step Teaching Flow

**Step 1 — Prepare the Telemetry Files**
*   **What you are doing:** Generating simulated device nodes pinging their statuses.
*   **Instruction:** Create `telemetry.json` and `telemetry.csv` inside `data/inbound/`. Include some missing timestamps and massive outlier values.

**Step 2 — Identify Hardware Drift (Jupyter)**
*   **What you are doing:** Profiling the machine data for obvious hardware faults.
*   **Instruction:** Build a Jupyter notebook plotting the `value` distribution. Call out the missing timestamps and the spikes in temperature that violate physical reality.

**Step 3 — Execute the Pipeline**
*   **What you are doing:** Loading the sanitized timeseries data.
*   **Instruction:** Run the ETL and query Postgres chronologically to view the streaming state.

**Step 4 — Inject Physical Outliers**
*   **What you are doing:** Triggering the IoT quality gate.
*   **Instruction:** Modify a row to report `humidity_pct=150`. Execute the ETL and watch the gate halt the payload before it corrupts the analytics warehouse. Run `pytest` to verify the metric-specific unit tests.

***

## Future Exercise 2: HR Applicant Intake (API + CSV)

**The Pitch:**
*This is an exercise for the student to implement by modifying the `src/` modules.*
This scenario introduces the complex realm of compliance and privacy. Students learn how to ingest PII (Personally Identifiable Information) while enforcing regulatory contracts and redacting sensitive data streams.

### 1. The Domain Requirements
*   **Target Schema (`raw_applicants`):** `partner_id` (string), `applicant_id` (string), `email` (string, regex validated), `phone` (string, optional, regex validated), `country` (string), `submitted_at` (datetime), `ingested_at` (datetime UTC).
*   **Quality Gate Rules:**
    *   `email` strictly conforms to an internet email regex.
    *   `country` strictly adheres to a predefined ISO allowed-list.
    *   `submitted_at` is heavily checked against future dates.
    *   Compound uniqueness: `(partner_id, applicant_id)`.

### 2. The Step-by-Step Teaching Flow

**Step 1 — Prepare the Applicant Files**
*   **What you are doing:** Gathering inbound resumes and application drops.
*   **Instruction:** Create the mock API and CSV candidate files.

**Step 2 — Build the PII Pipeline**
*   **What you are doing:** Extracting the data while avoiding logging sensitive credentials or tokens.
*   **Instruction:** When running the ETL process (`docker compose run --rm etl`), explicitly point out to the audience that your `logger.info()` lines are *scrubbed* of any actual names, emails, or phone numbers. Explain why PII must never enter the raw console logs.

**Step 3 — Validate Data Sovereignty**
*   **What you are doing:** Enforcing the allowed `country` list.
*   **Instruction:** Introduce a payload originating from a non-compliant or embargoed jurisdiction. Show Great Expectations rejecting the application intake automatically based on the ISO list rule.
