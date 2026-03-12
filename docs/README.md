# Documentation Hub

> [!NOTE]
> Welcome to the central documentation index for the **Fraud-Ready Payments Data Engineering Lab**. This hub is designed to help you navigate project setup, operational runbooks, architectural designs, and hands-on demos.

---

## 🏗️ 1. Build & Infrastructure
**Essential guides for setting up the lab, managing infrastructure, and CI/CD pipelines.**

- [**Command Cheatsheet**](build/00-cheatsheet.md) - Quick reference for Docker, Postgres, and ETL commands.
- [**CI/CD (GitHub Actions)**](build/05-ci-github-actions.md) - Overview of the automated testing and validation workflows.
- [**GitHub Multi-Account Auth**](build/10-github-multi-account-auth.md) - How to manage multiple GitHub identities.

---

## 📋 2. SOPs & Operations
**Standard Operating Procedures for running and maintaining the data pipeline.**

- [**SOP / Runbook**](operations/01-sop-runbook.md) - The step-by-step operational guide for the ETL process.
- [**System Admin Guide (SOP)**](operations/02-admin-guide.md) - Admin-level platform maintenance and reliability guide.
- [**Troubleshooting Guide**](operations/04-troubleshooting.md) - Known issues, log extraction, and recovery procedures.

---

## 🏗️ 3. Architecture & Specifications
**Technical blueprints and design contracts for the data platform.**

- [**System Architecture**](architecture/02-architecture.md) - Higher-level design of the Postgres/Python/Docker stack.
- [**Data Quality & Testing**](architecture/03-quality-and-testing.md) - Deep dive into Great Expectations and Pytest strategies.
- [**Product Spec: Fraud Payments**](architecture/06-project-spec-fraud-payments.md) - The business requirements and technical schema.

---

## 🚀 4. Hands-on Demos
**Step-by-step guides for showcasing the platform's features.**

- [**Demos Curriculum Index**](demos/README.md) - The master hub for all demo scenarios.
- [**Demo 1: Fraud-Ready Payments**](demos/01-fraud-payments/walkthrough.md) - Ingesting API/CSV financial data with strict gates.
- [**Demo 2: IoT Sensor Telemetry**](demos/02-iot-telemetry/walkthrough.md) - High-volume time-series data with partitioning and physical gates.
- [**Demo 3: HR Applicant Intake**](demos/03-hr-applicants/walkthrough.md) - Privacy, PII Redaction, and Compliance.
- [**Demo 4: Streaming Event Platform**](demos/04-streaming-platform/walkthrough.md) - Real-time Kafka-Spark ingestion with Medallion Delta Lake.
- [**Demo 5: Orchestration & Governance**](demos/05-orchestration/walkthrough.md) - Airflow SLAs and platform reliability.
- [**Demo 6: Proactive Data Observability**](demos/06-observability/walkthrough.md) - Statistical drift detection and metrics monitoring.

---

## 🎓 5. Career & Portfolio
**Resources to help showcase this platform to hiring managers and technical interviewers.**

- [**Resume Project Bullets**](12-resume-project-bullets.md) - senior-level project descriptions for your CV.
- [**Interview Slide Deck Outline**](13-slide-deck-outline.md) - Technical walkthrough slides and architecture talking points.
- [**Interview Q&A (DRE/Platform)**](08-interview-qa.md) - Curated questions and senior-level answers based on this lab.
- [**OCI Cloud Mapping Guide**](10-oci-cloud-mapping.md) - Design plan for cloud migration (Always Free Tier).
