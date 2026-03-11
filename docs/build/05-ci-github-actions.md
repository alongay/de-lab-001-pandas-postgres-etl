# Continuous Integration (CI): GitHub Actions

This repository utilizes GitHub Actions to enforce code quality and prevent broken data engineering logic from ever merging into the main branch. 

---

## 1. The CI Strategy

**What it does:** Every time a developer opens a Pull Request or pushes to `main`, GitHub spins up an isolated Ubuntu server, checks out this code, boots the exact Docker Compose environment we use locally, and runs our tests.

**Why we do this:** Without automated testing, a developer might accidentally push a syntax error in `src/transform_payments.py` that would subsequently crash the production pipeline. The CI environment guarantees that every single code change is mathematically verified before being allowed to merge.

**The Workflow File Location:** `.github/workflows/ci.yml`

---

## 2. The Testing Pipelines (Jobs)

The CI workflow is split into two escalating phases of verification.

### Phase 1: `unit-tests`
*   **When it runs:** On every Pull Request and immediately on pushes to `main`.
*   **What happens:** GitHub builds the `etl` Docker image and executes `docker compose run --rm etl pytest`.
*   **Why this phase exists:** It provides incredibly fast feedback (usually < 1 minute) to the developer. Because the unit test suite natively falls back to an in-memory SQLite database, it does not have to waste time booting the heavy PostgreSQL image.

### Phase 2: `integration-smoke`
*   **When it runs:** *Only* on pushes to the `main` branch, and *only* if the `unit-tests` phase passes first.
*   **What happens:** GitHub fully boots the heavy PostgreSQL background database (`docker compose up -d --build postgres`). It waits for the database to become healthy, and then runs the actual production ETL command (`docker compose run --rm etl`). 
*   **Why this phase exists:** Pure unit tests can miss real-world infrastructure problems (like networking bugs, authentication drift, or Postgres-specific dialing issues). This job actually proves the end-to-end wiring of the platform using a synthetic `.env` file!

---

## 3. Retrieving Audit Artifacts

If a test fails, you need to know exactly *why* it failed. To help with this, our CI runner automatically extracts the Great Expectations validation JSON from the Docker container and uploads it securely to the GitHub UI.

**How to find a failed test report:**
1. Navigate to the **Actions** tab in your GitHub repository.
2. Click on the failed workflow run (marked with a red X).
3. Scroll to the very bottom of the summary page to the **Artifacts** section.
4. Download either `ge-artifacts-unit-tests` or `ge-artifacts-integration`.
5. Unzip the file and open the `logs/ge_validation_<timestamp>.json` document. Look for `success: false` and review the "unsuccessful expectations" array to identify exactly which validation rule blocked the deployment!

---

## 4. Security Principles
*   **Zero Secrets in CI:** The CI runner does not need access to live production API keys or Databricks tokens. It strictly consumes synthetic dummy variables generated directly from the `.env.example` file.
*   **Ephemeral Data:** The PostgreSQL database spun up during the integration test is immediately destroyed at the end of the Job. No data persists.
