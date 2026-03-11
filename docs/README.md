# Documentation Hub

Welcome to the central documentation index for the **Fraud-Ready Payments Data Engineering Lab**. This hub is designed to help you navigate project setup, operational runbooks, architectural designs, and hands-on demos.

---

## 🛠️ Build & Infrastructure
*Essential guides for setting up the lab, managing infrastructure, and CI/CD pipelines.*

*   [**Command Cheatsheet**](build/00-cheatsheet.md) - Quick reference for Docker, Postgres, and ETL commands.
*   [**CI/CD (GitHub Actions)**](build/05-ci-github-actions.md) - Overview of the automated testing and validation workflows.
*   [**GitHub Multi-Account Auth**](build/10-github-multi-account-auth.md) - How to manage multiple GitHub identities (`AISavantGH` vs `alongay`).

---

## 📋 SOPs & Operations
*Standard Operating Procedures for running and maintaining the data pipeline.*

*   [**SOP / Runbook**](operations/01-sop-runbook.md) - The step-by-step operational guide for the ETL process.
*   [**Troubleshooting Guide**](operations/04-troubleshooting.md) - Known issues, log extraction, and recovery procedures.

---

## 🏗️ Architecture & Specifications
*Technical blueprints and design contracts for the data platform.*

*   [**System Architecture**](architecture/02-architecture.md) - Higher-level design of the Postgres/Python/Docker stack.
*   [**Data Quality & Testing**](architecture/03-quality-and-testing.md) - Deep dive into Great Expectations and Pytest strategies.
*   [**Product Spec: Fraud Payments**](architecture/06-project-spec-fraud-payments.md) - The business requirements and technical schema for the payments domain.

---

## 🚀 Hands-on Demos
*Step-by-step guides for showcasing the platform's features.*

*   [**Demos Curriculum Index**](demos/README.md) - The master hub for all demo scenarios.
*   [**Demo 1: Fraud-Ready Payments**](demos/01-fraud-payments/walkthrough.md) - Ingesting API/CSV financial data with strict gates.
*   [**Demo 1: Chaos Run**](demos/01-fraud-payments/chaos-run.md) - Simulating failures and archiving quality artifacts.
