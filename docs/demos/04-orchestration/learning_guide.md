# Demo 4 Learning Guide: Enterprise Orchestration & SLA Governance

This guide explains the "Senior DE" rationale behind the patterns implemented in Demo 4.

## 1. Batch vs. Streaming: Use the Right Pattern
In production, we treat Batch and Streaming differently within an orchestrator like Airflow.

### **Batch Pattern: Direct Ownership**
For the **Payments ETL Pipeline**, Airflow is the "Master of Fate."
- **Schedule**: It knows exactly when the task should start.
- **Dependency**: It validates that the CSV is present before starting.
- **Status**: It tracks success/failure directly based on the container exit code.
- **Audit**: It verifies the Great Expectations (GE) artifact before completing.

### **Streaming Pattern: Operational Monitoring (Health & SLA)**
For **IoT Streaming**, Airflow is the "Silent Guardian."
- **Why?**: Streaming jobs are typically long-running (24/7). Restarting them on every Airflow schedule is inefficient and dangerous.
- **SLA Checks**: Airflow monitors the **Delta Lake logs**. If no new commits are made within 5 minutes, Airflow triggers a failure.
- **Connectivity Pulse**: It checks if Kafka is reachable on the platform network.
- **Result**: You get the benefits of Airflow alerting without the overhead of trying to manage long-running process lifecycles.

## 2. Infrastructure Patterns

### **Port Isolation (8088 vs 8080)**
Conflict management is a key operational skill. By remapping Airflow to **8088**, we prevent collisions with the Spark Master UI, ensuring both monitoring surfaces are available simultaneously.

### **Shared Networking (`pde_platform_net`)**
Rather than relying on default "ambiguous" bridge networks, we established a **dedicated external network**.
- **Service Discovery**: Allows Airflow to reach `postgres` or `iot-kafka` by their container names.
- **Security**: Isolates platform traffic to an intentional group of services.

### **LocalExecutor Optimization**
For local development, **LocalExecutor** is the $0 sweet spot.
- **Parallelism**: Runs tasks as sub-processes on the scheduler.
- **Simplicity**: Avoids the cost and overhead of Redis/RabbitMQ and Celery workers required for larger clusters.

## 3. Operational Signals (Interview "Gold")
When presenting this demo, focus on these three signals:
1. **Governance Pulse**: "My DAG doesn't just run code; it verifies that the Quality Gate artifact exists."
2. **Freshness Monitoring**: "I use Airflow to monitor my Streaming SLA by calculating Delta Log age."
3. **Failure Callbacks**: "Every task failure triggers a mock PagerDuty/Slack alert for realistic operational response."
