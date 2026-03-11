# Cost Model — Enterprise Data Platform (v2026.3.11)

This lab is designed for **$0 Operational Cost** using local containerization.

## 1. Resource Consumption (Local)
| Component | Technology | Cost (Local) |
| :--- | :--- | :--- |
| Database | PostgreSQL 15 | $0 |
| Event Bus | Kafka (KRaft) | $0 |
| Compute | Spark 3.5.1 | $0 |
| Warehouse | Delta Lake (Local) | $0 |
| Orchestration | PowerShell / Make | $0 |

## 2. Cloud Transition (PAYG)
> [!NOTE]
> Moving this lab to Production (GCP) would incur the following estimated costs:

| Component | Target Service | Est. Monthly Cost (Low Traffic) |
| :--- | :--- | :--- |
| Ingestion | Cloud Pub/Sub | ~$0.10 (First 10GB free) |
| Compute | Cloud Run / GKE | ~$30 - $150 (Autoscaling) |
| Analytics | BigQuery / Cloud Storage | ~$5 - $20 |
| Monitoring | Cloud Logging/Trace | ~$2.00 / GB |

## 3. Cost Per 1,000 Users/Month
- **Local Development**: $0.00
- **Production (Estimated)**: **$0.45** (Assuming 1k small event batches per user)

**Summary: $0 -> PAYG REQUIRED**
