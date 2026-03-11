# Demo 2: IoT Sensor Telemetry

**Status: ✅ Implemented & Verified**

### 🎯 The Pitch
This demo shifts focus to **"Material Reality."** We simulate a high-volume IoT environment where thousands of sensors upload data. The challenge is ensuring that **hardware failures** or **sensor drift** don't corrupt analytical models.

### 🛠️ Technical Challenges
- **Time-Series Deduplication**: Handling millions of pings while ensuring uniqueness.
- **Physical Bounds Checking**: Validating metrics against **physical reality** (e.g., rejecting humidity > 100%).
- **Metric-Unit Consistency**: Preventing **"Unit Mismatch"** bugs (e.g., Fahrenheit vs. Celsius).

### 🎓 Teaching Flow
- **High-Volume Mocking**: Generate a CSV containing thousands of readings with **ghost outliers**.
- **Visual Profiling**: Use **JupyterLab** to plot sensor graphs, making faults visually apparent.
- **Physical Gate**: Configure **Great Expectations** to act as a **"physics engine."**
- **Batch Quarantine Pattern**: Watch the pipeline automatically **quarantine** impossible readings.

---
**Links:**
- [**Walkthrough Script**](walkthrough.md)
- [**Chaos Run Execution**](chaos-run.md)
