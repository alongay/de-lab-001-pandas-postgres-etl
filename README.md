# Enterprise Data Engineering Demo Platform

A production-style data engineering portfolio that demonstrates how to build, validate, operate, and observe modern data pipelines across **batch ETL**, **time-series telemetry**, **real-time streaming**, **orchestration**, and **cloud mapping**.

This repository is designed to show how data engineers go beyond moving data from one system to another. It focuses on building pipelines that are:

- **correct** through strict validation and schema enforcement
- **resilient** through quarantine and failure isolation
- **replayable** through raw data preservation
- **observable** through freshness, SLA, and health monitoring
- **production-shaped** through orchestration, partitioning, and cloud-aligned architecture

## What’s inside

The platform is organized as a connected set of demos that build on one another:

- **Demo 1 — Payments ETL:** batch ingestion, Great Expectations, staging/promote, canonical outputs
- **Demo 2 — IoT Batch Telemetry:** physical validation, UTC normalization, partitioning, quarantine
- **Demo 3 — IoT Streaming Platform:** Kafka, Spark Structured Streaming, Delta Bronze/Silver, anomaly routing
- **Demo 4 — Orchestration & SLA Governance:** Airflow, retries, freshness checks, alerting
- **Demo 5 — Observability:** validation artifacts, Delta log freshness, quarantine growth monitoring
- **Demo 6 — OCI Cloud Mapping:** local-to-cloud platform blueprint for Oracle Cloud Infrastructure

## Core technologies

`Python` · `SQL` · `PostgreSQL` · `Great Expectations` · `Kafka` · `Spark Structured Streaming` · `Delta Lake` · `Airflow` · `Docker` · `OCI`

## Why this project matters

This repo is built to answer an important engineering question:

> How do you design data systems that remain trustworthy when data is incomplete, wrong, duplicated, delayed, or physically impossible?

The answer, demonstrated throughout this project, is to combine:

- validation gates
- quarantine patterns
- replayable raw layers
- clean curated outputs
- orchestration and retries
- observability and freshness monitoring

## Repository structure

This repository is organized as a **domain-oriented data platform** so each demo remains isolated, testable, and easy to extend while shared platform capabilities stay reusable.

```text
.
├── src/                    # Core application logic and domain ETL modules
│   ├── core/               # Shared utilities (DB, config, logging, observability hooks)
│   ├── payments/           # Demo 01: Payments ETL / fraud-style validation
│   ├── iot/                # Demo 02: Batch IoT telemetry pipeline
│   ├── hr/                 # Demo 03: HR privacy / compliance pipeline
│   ├── streaming/          # Demo 04: Kafka + Spark + Delta streaming logic
│   └── orchestration/      # Demo 05: Airflow orchestration and platform monitoring
│
├── docs/                   # Documentation hub
│   ├── demos/              # Demo walkthroughs, specs, and chaos-run guides
│   ├── architecture/       # System diagrams and design documents
│   ├── build/              # Infrastructure, setup, CI/CD, and cloud mapping
│   ├── operations/         # SOPs, runbooks, troubleshooting, and checklists
│   └── assets/             # Screenshots, banners, proof-pack visuals
│
├── scripts/                # Data generation and operational helper scripts
│   ├── payments/           # Payment demo generators and helpers
│   ├── iot/                # Sensor data generators and telemetry helpers
│   └── ...                 # Symmetrical layout for additional domains
│
├── notebooks/              # Domain-specific exploration and validation notebooks
│   ├── payments/           # Fraud analysis and profiling
│   ├── streaming/          # Delta Lake audits and streaming validation
│   └── ...                 # Symmetrical layout for additional domains
│
├── data/                   # Isolated persistence layers and demo data
│   ├── payments/           # Batch landing zones and relational demo storage
│   ├── streaming/          # Delta Lake tables, checkpoints, and stream artifacts
│   └── ...                 # Symmetrical layout for additional domains
│
├── orchestration/          # Apache Airflow control plane
│   ├── dags/               # DAGs for orchestration, SLA, and freshness monitoring
│   └── plugins/            # Custom Airflow operators and helpers
│
├── tests/                  # Pytest suite and QA gates
│   ├── core/               # Shared logic tests
│   ├── payments/           # Payments domain tests
│   ├── iot/                # IoT domain tests
│   └── ...                 # Symmetrical layout for additional domains
│
├── task.ps1                # PowerShell task runner
├── docker-compose.yml      # Core platform services
├── docker-compose.*.yml    # Domain-specific isolated stacks
└── README.md               # Showcase entry point
```

### Design principles behind the structure

* **Domain isolation:** Each demo has its own logic, scripts, data, and notebooks so changes in one area do not create unnecessary coupling in another.
* **Shared core utilities:** Common services such as database access, configuration, and observability hooks live in `src/core/` and are reused across domains.
* **Documentation-first layout:** Architecture, operations, build guidance, and demo walkthroughs are separated so the repo works as both a portfolio and a study resource.
* **Operational symmetry:** Scripts, notebooks, data, and tests follow the same domain pattern wherever possible, making the repository easier to navigate and scale.
* **Platform control plane separation:** Airflow orchestration is kept at the platform level because it supervises pipelines rather than behaving like a single domain ETL module.

## Best way to read this repo

1. Start with the [architecture overview](file:///docs/architecture/README.md)  
2. Review the [demo catalog](file:///docs/demos/README.md)  
3. **Master the platform** with the [Hands-on Mastery Guide](file:///docs/operations/hands-on-mastery-guide.md)
4. Run one batch demo  
5. Run one streaming demo  
6. Review orchestration and observability docs  
7. Explore cloud mapping and interview artifacts
