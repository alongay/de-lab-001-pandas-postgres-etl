SHELL := /bin/bash

.PHONY: help up down ps logs etl test smoke rebuild clean demo-payments

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

ps:
	docker compose ps

logs:
	docker compose logs -f --tail 200

etl: assert-env
	docker compose run --rm etl

test:
	docker compose run --rm etl pytest

smoke: assert-env
	docker compose up -d --build postgres
	docker compose run --rm etl
	docker compose down

rebuild: assert-env
	docker compose down
	docker compose build --no-cache
	docker compose up -d
	docker compose ps

clean:
	docker compose down -v

demo-payments: assert-env
	@echo -e "\n=== 1. Starting Services ==="
	docker compose up -d --build
	
	@echo -e "\n=== 2. Generating Demo Data ==="
	bash ./scripts/create_payments_demo_data.sh

	@echo -e "\n=== 3. Resetting Database State ==="
	sleep 3
	docker exec pde_postgres_15 sh -lc "psql -P pager=off -U de_user -d de_workshop -c 'TRUNCATE TABLE raw_payments;'" || true

	@echo -e "\n=== 4. Running Happy Path (both sources) ==="
	INGEST_SOURCE=both docker compose run --rm etl

	@echo -e "\n=== 5. Injecting Chaos (Negative Amount) ==="
	@echo "txn_id,account_id,amount,currency,status,txn_ts" > data/inbound/transactions_daily.csv
	@echo "TXN-30001,ACCT-9001,49.95,USD,CAPTURED,2026-03-01T12:34:56Z" >> data/inbound/transactions_daily.csv
	@echo "TXN-30002,ACCT-9002,-75.50,USD,CAPTURED,2026-03-01T12:35:56Z" >> data/inbound/transactions_daily.csv
	@echo "TXN-30003,ACCT-9003,75.50,USD,DECLINED,2026-03-01T12:36:56Z" >> data/inbound/transactions_daily.csv

	@echo -e "\n=== 6. Expected Failure (Great Expectations catches bad data) ==="
	INGEST_SOURCE=csv docker compose run --rm etl || true
	@echo -e "\nLook in logs/ for the generated GE artifact detailing the failure.\n"

	@echo -e "\n=== 7. Proving Recovery (Fixing CSV) ==="
	bash ./scripts/create_payments_demo_data.sh > /dev/null
	INGEST_SOURCE=csv docker compose run --rm etl

	@echo -e "\n=== 8. Archiving Chaos Artifact ==="
	mkdir -p artifacts
	ls -t logs/ge_validation_*.json | head -1 | xargs -I {} cp {} artifacts/latest_chaos_failure.json || true
	@echo "Copied GE failure log to artifacts/latest_chaos_failure.json"

	@echo -e "\n=== 9. Tearing down services ==="
	docker compose down
	@echo -e "\nDemo run complete!"
