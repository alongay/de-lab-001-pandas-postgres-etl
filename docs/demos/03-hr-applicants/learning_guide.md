# PII & Data Sovereignty: The DE Compliance Edge

## Why Privacy Matters in DE?
Data Engineering isn't just about moving bits; it's about moving bits **legally**. For an enterprise, a PII leak is a multi-million dollar liability.

**Example**: You ingest applicant data from the EU.
- **Problem**: You cannot store the original `full_name` or `email` in a US-based cloud without strict legal hurdles.
- **Solution**: Redact or tokenize at the point of ingestion (The "Gateway" pattern).

## The Redaction Pattern in the Lab
The Lab uses a strict **Transformer-level Redaction**:
1.  **Extraction**: Raw applicant data arrives via API or CSV.
2.  **Transformation**: The `RedactPii` class intercepts the data.
3.  **Physical Masking**: Sensitive strings are replaced with `[REDACTED]` *before* they ever hit the database.
4.  **Failure Pattern**: If a "High Risk" country is detected (sovereignty audit), the record is quarantined to `hr_applicants_quarantine`.

## Interview Talking Point
> "I implemented a privacy-first ingestion pipeline that uses automated PII redaction and sovereignty-based routing. This ensured that sensitive applicant data never landed in the primary store for non-compliant regions, lowering the platform's risk profile."
