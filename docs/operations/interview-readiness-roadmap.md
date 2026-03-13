# 🚀 The "Off-Hand" Interview Readiness Roadmap

To transition from building this platform to **explaining it with authority**, follow this 72-hour acceleration plan. This will help you "know the stuff" without looking at your notes.

---

## ⏱️ The 3-Day Acceleration Plan

### Day 1: The "Destructive Learning" Drill
**Goal**: Internalize dependencies by breaking the system.
1.  **Break it**: Manually stop the `iot-postgres` container while the Airflow DAG is running. 
2.  **Explain it**: Verbally describe what just happened to the *Metadata Layer* and the *Retry Logic*.
3.  **Fix it**: Use `.\task.ps1` to restore state.
4.  **The "Senior" Marker**: If you can explain *why* Docker networking fixed the HR loader, you've mastered the Platform layer.

### Day 2: The "Verbal Walkthrough"
**Goal**: Build muscle memory for technical storytelling.
1.  **Open the dashboards**: [http://localhost:3010](http://localhost:3010).
2.  **Describe the flow**: Point at the "Executive Watchtower" and explain the Journey of a single sensor reading:
    - *Kafka Topic* -> *Spark Bronze (Raw)* -> *GX Quality Gate* -> *Spark Silver (Cleaned)* -> *Metabase Visualization*.
3.  **Practice the Pitch**: Record yourself giving a 2-minute summary of the **BI-as-Code** CLI.

### Day 3: The "Whiteboard Pressure"
**Goal**: Master the "Why" behind the "How".
1.  **Challenge**: Draw the Medallion architecture on a piece of paper from memory.
    - Did you remember the **Quarantine** bucket?
    - Did you remember the **Airflow** control plane?
2.  **STAR Scenarios**: Review the [**Resume Deep Dives**](../14-resume-deep-dives.md) and practice the "Chaos Injection" story.

---

## 💡 The "Big Three" Soundbites (Memorize These)

1.  **On Data Quality**: 
    > *"I implemented specialized **GX Gates** that act as the 'Data Police,' diverting out-of-bounds telemetry to quarantine rather than letting it poison our production dashboards."*

2.  **On Infrastructure**: 
    > *"I treated our entire BI layer as **BI-as-Code**, using a custom Python CLI to manage dashboard configurations in Git, ensuring 100% reproducibility across environments."*

3.  **On Orchestration**: 
    > *"I used **Apache Airflow** as the central nervous system, decoupling our ETL logic from execution to handle retries, sensors, and cross-domain SLAs automatically."*

---

## 🛠️ Self-Check Quiz (The "Final 10")
1.  What is the difference between **Bronze** and **Silver** data?
2.  Why did we use a **Medallion Architecture** instead of a flat table?
3.  What happens to a sensor reading that is over **500°C**?
4.  What is an **Idempotent** script?
5.  How do we handle **Silent Data Drift**?
6.  Why did we switch from `localhost` to `postgres` in the HR loader?
7.  What is the role of the **`_delta_log`**?
8.  How does the **Metabase CLI** help a Platform Team?
9.  Why use **Kafka** instead of inserting directly into a DB?
10. What is the business value of the **"Executive Watchtower"**?

---

**If you can answer these confidently, you are ready to get hired.** 🚀🏙️💎🏁🏆
