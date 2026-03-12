# Medallion Architecture: High-Velocity Streaming Patterns

## Why Medallion Architecture?
In streaming, you don't just "dump data". You refine it. The Medallion architecture (Bronze/Silver/Gold) provides a structured path for data quality.

1.  **Bronze (Raw)**: Captures events Exactly-Once from Kafka. Minimal transformation. This is your "Source of Truth".
2.  **Silver (Refined)**: Handles deduplication, schema enforcement, and partitioning. This is where business-ready entities live.
3.  **Gold (Aggregated)**: Business-level KPIs (e.g., Transactions per Minute).

## The Streaming Pattern in the Lab
The Lab uses **Spark Structured Streaming** with **Delta Lake**:
- **Kafka**: The message broker holding raw sensor events.
- **Micro-batches**: Spark polls Kafka every 5 seconds to ingest newly arrived events.
- **Checkpointing**: Ensures that if the pipeline crashes, it resumes exactly where it left off (No data loss).
- **Quarantine**: Events failing basic validation (e.g., missing timestamps) are routed to a separate quarantine table, keeping the Silver layer clean.

## Interview Talking Point
> "I designed a Medallion-based streaming pipeline using Spark and Delta Lake. By implementing micro-batch checkpointing and a dedicated quarantine layer for anomalies, I achieved Exactly-Once processing guarantees even in high-velocity IoT scenarios."
