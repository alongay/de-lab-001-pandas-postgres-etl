# Statistical Drift: The DE Interview Edge

## What is Data Drift?
In production, data quality isn't just about "Does this column have nulls?". It's about "Is the shape of the data still what the model/business expects?".

**Example**: You monitor transaction amounts.
- **Week 1**: Mean=$50, StdDev=$10.
- **Week 2**: Mean=$950, StdDev=$5 (even if no nulls and all types are correct).
- **Result**: Downstream fraud models might break or produce false alerts.

## The Kolmogorov-Smirnov (KS) Test
The Lab uses the **KS-Test** to detect these shifts.
- **How it works**: It compares the Cumulative Distribution Function (CDF) of two samples.
- **P-Value**: If the $p$-value is $< 0.05$, there is a high probability that the distributions have shifted.

## Enterprise Implementation in the Lab
We separate the **Audit** from the **Compute**:
1.  **Extraction**: Raw data lands.
2.  **Transformation**: Data is cleaned.
3.  **Observability Injection**: A lightweight fingerprint of the distribution is saved to the **Metadata Lake** (DuckDB).
4.  **Asynchronous Audit**: Airflow (or a dedicated monitoring service) audits the DuckDB store to detect drift across the platform.

## Interview Talking Point
> "I implemented a proactive observability layer that uses statistical distribution checks. This detected 'silent failures' like mean shifts in financial columns that Great Expectations wouldn't catch with simple range checks."
