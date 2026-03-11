# Demo 2: IoT Sensor Telemetry

**Status: ⏳ Next Phase**

### 🎯 The Pitch
This demo shifts focus from "Money" to **"Material Reality."** We simulate a high-volume IoT environment where thousands of sensors upload temperature and humidity data. The challenge is ensuring that hardware failures or "sensor drift" don't corrupt our analytical models.

### 🛠️ Technical Challenges
*   **Time-Series Deduplication**: Handling millions of pings while ensuring uniqueness on `(device_id, reading_ts, metric)`.
*   **Physical Bounds Checking**: Validating metrics against physical reality (e.g., rejecting humidity > 100% or temps exceeding hardware specs).
*   **Metric-Unit Consistency**: Preventing "Unit Mismatch" bugs (e.g., receiving Fahrenheit values labeled as Degrees Celsius).

### 🎓 Teaching Flow
1.  **High-Volume Mocking**: Generate a CSV containing thousands of readings with intentional "ghost" outliers.
2.  **Visual Profiling**: Use JupyterLab to plot sensor graphs, making "hardware faults" visually apparent.
3.  **Physical Gate**: Configure Great Expectations to act as a "physics engine," blocking impossible readings.
4.  **Chaos Run**: Inject an "impossible reading" batch and watch the pipeline automatically quarantine it.
