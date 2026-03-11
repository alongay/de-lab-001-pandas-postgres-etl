SHELL := /bin/bash

.PHONY: help up down ps logs etl test smoke rebuild clean demo-payments demo-iot demo-iot-stream

help:
	@echo "Targets:"
	@echo "  up      - Build and start services (Postgres + Jupyter)"
	@echo "  down    - Stop services"
	@echo "  ps      - Show service status"
	@echo "  logs    - Tail logs"
	@echo "  etl     - Run ETL once (one-off container)"
	@echo "  test    - Run pytest in container"
	@echo "  smoke   - Start Postgres, run ETL, then stop"
	@echo "  rebuild - Full rebuild (no-cache)"
	@echo "  clean   - Destructive: down -v (removes DB volume)"
	@echo "  demo-payments    - Runs the Fraud-Ready Payments demo"
	@echo "  demo-iot         - One-command IoT pipeline demo"
	@echo "  demo-iot-stream  - One-command Enterprise Streaming demo (Kafka+Spark+Delta)"

assert-env:
	@if [ ! -f .env ]; then \
		echo "Missing .env. Create it from .env.example:"; \
		echo "  cp .env.example .env"; \
		exit 1; \
	fi

up: assert-env
	docker compose up -d --build
	docker compose ps

down:
	docker compose down
	docker compose -f docker-compose.streaming.yml down 2>/dev/null || true

ps:
	docker compose ps

logs:
	docker compose logs -f --tail 200

DOMAIN ?= payments
etl: assert-env
	docker compose run --rm -e PYTHONPATH=/app etl python -m src.$(DOMAIN).etl_run_$(DOMAIN)

test:
	docker compose run --rm -e PYTHONPATH=/app etl pytest

smoke: assert-env
	docker compose up -d --build postgres
	docker compose run --rm etl python -m src.payments.etl_run_payments
	docker compose down

rebuild: assert-env
	docker compose down
	docker compose build --no-cache
	docker compose up -d
	docker compose ps

clean:
	docker compose down -v
	docker compose -f docker-compose.streaming.yml down -v 2>/dev/null || true

demo-payments: assert-env
	@echo -e "\n=== 1. Starting Services ==="
	docker compose up -d --build
	
	@echo -e "\n=== 2. Generating Demo Data ==="
	bash ./scripts/payments/create_payments_demo_data.sh
	
	@echo -e "\n=== 3. Initializing / Resetting Database State ==="
	sleep 3
	docker compose run --rm -e PYTHONPATH=/app etl python -m scripts.payments.init_payments_db
	docker exec pde_postgres_15 sh -lc "psql -P pager=off -U de_user -d de_workshop -c 'TRUNCATE TABLE raw_payments;'" || true

	@echo -e "\n=== 4. Running Happy Path (both sources) ==="
	INGEST_SOURCE=both docker compose run --rm etl python -m src.payments.etl_run_payments

	@echo -e "\n=== 5. Injecting Chaos (Negative Amount) ==="
	@echo "txn_id,account_id,amount,currency,status,txn_ts" > data/payments/transactions_daily.csv
	@echo "TXN-30001,ACCT-9001,49.95,USD,CAPTURED,2026-03-01T12:34:56Z" >> data/payments/transactions_daily.csv
	@echo "TXN-30002,ACCT-9002,-75.50,USD,CAPTURED,2026-03-01T12:35:56Z" >> data/payments/transactions_daily.csv
	@echo "TXN-30003,ACCT-9003,75.50,USD,DECLINED,2026-03-01T12:36:56Z" >> data/payments/transactions_daily.csv

	@echo -e "\n=== 6. Expected Failure (Great Expectations catches bad data) ==="
	INGEST_SOURCE=csv docker compose run --rm etl python -m src.payments.etl_run_payments || true
	@echo -e "\nLook in logs/ for the generated GE artifact detailing the failure.\n"

	@echo -e "\n=== 7. Proving Recovery (Fixing CSV) ==="
	bash ./scripts/payments/create_payments_demo_data.sh > /dev/null
	INGEST_SOURCE=csv docker compose run --rm etl python -m src.payments.etl_run_payments

	@echo -e "\n=== 8. Archiving Chaos Artifact ==="
	mkdir -p artifacts
	ls -t logs/ge_validation_*.json | head -1 | xargs -I {} cp {} artifacts/latest_chaos_failure.json || true
	@echo "Copied GE failure log to artifacts/latest_chaos_failure.json"

	@echo -e "\n=== 9. Tearing down services ==="
	docker compose down
	@echo -e "\nDemo run complete!"

demo-iot: assert-env
	@echo -e "\n=== 1. Starting Services (IoT Mode) ==="
	docker compose up -d --build
	
	@echo -e "\n=== 2. Resetting Database (IoT Tables) ==="
	sleep 3
	docker exec pde_postgres_15 sh -lc "psql -P pager=off -U de_user -d de_workshop -c 'TRUNCATE TABLE raw_sensor_readings, raw_sensor_readings_quarantine CASCADE;'" || true

	@echo -e "\n=== 3. Running Happy Path (Low Outliers) ==="
	DEVICE_COUNT=10 MINUTES=30 OUTLIER_RATE=0.0 MISSING_TS_RATE=0.0 bash ./scripts/iot/create_iot_demo_data.sh
	docker compose run --rm -e PYTHONPATH=/app etl python -m src.iot.etl_run_iot

	@echo -e "\n=== 4. Injecting Chaos (High Outliers) ==="
	DEVICE_COUNT=10 MINUTES=30 OUTLIER_RATE=0.8 MISSING_TS_RATE=0.0 bash ./scripts/iot/create_iot_demo_data.sh
	docker compose run --rm -e PYTHONPATH=/app etl python -m src.iot.etl_run_iot || true
	@echo -e "\nExpected failure due to the Quarantine Pattern."

	@echo -e "\n=== 5. Verifying Data Partitioning ==="
	docker exec pde_postgres_15 sh -lc "psql -P pager=off -U de_user -d de_workshop -c 'SELECT metric, COUNT(*) FROM raw_sensor_readings GROUP BY metric;'"
	@echo "--- Quarantine Table ---"
	docker exec pde_postgres_15 sh -lc "psql -P pager=off -U de_user -d de_workshop -c 'SELECT metric, COUNT(*) FROM raw_sensor_readings_quarantine GROUP BY metric;'"

	@echo -e "\n=== 6. Tearing down services ==="
	docker compose down
	@echo -e "\nIoT Demo complete!"

demo-iot-stream: assert-env
	@echo -e "\n=== 1. Starting Infrastructure (Option A: Separate Compose) ==="
	docker compose -f docker-compose.yml -f docker-compose.streaming.yml up -d --build iot-kafka iot-spark-master iot-spark-worker
	
	@echo -e "\n=== 2. Creating Kafka Topics ==="
	sleep 10
	bash ./scripts/streaming/create_kafka_topic.sh

	@echo -e "\n=== 3. Starting Medallion Pipelines (Bronze -> Silver) ==="
	docker compose -f docker-compose.yml -f docker-compose.streaming.yml up -d iot-bronze-stream iot-silver-stream
	
	@echo -e "\n=== 4. Starting Event Producer (Injecting Chaos) ==="
	docker compose -f docker-compose.yml -f docker-compose.streaming.yml up -d iot-stream-producer
	
	@echo -e "\n=== 5. Monitoring Pipeline (Waiting for Data) ==="
	@echo "Streaming is live. Observe the Spark jobs at http://localhost:8080"
	sleep 25
	
	@echo -e "\n=== 6. Verifying Data Landing (Medallion Layers) ==="
	docker exec pde-jupyter-lab ls -R /app/data/iot/delta/bronze
	docker exec pde-jupyter-lab ls -R /app/data/iot/delta/silver
	
	@echo -e "\n=== 7. Chaos Check (Quarantine) ==="
	@echo "Scanning for flagged anomalies in the Quarantine Delta Table..."
	docker exec pde-jupyter-lab python -c "import os; print('Anomalies Detected!' if os.path.exists('/app/data/iot/delta/quarantine') else 'No Anomalies Yet (Waiting...)')"

	@echo -e "\n=== 8. Tearing down streaming platform ==="
	docker compose -f docker-compose.yml -f docker-compose.streaming.yml down
	@echo -e "\nStreaming Demo complete!"
