#!/usr/bin/env bash
set -euo pipefail

DEVICE_COUNT="${1:-25}"
MINUTES="${2:-60}"
OUTLIER_RATE="${3:-0.03}"
MISSING_TS_RATE="${4:-0.01}"

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REPO_DIR="$(dirname "$(dirname "$DIR")")"
mkdir -p "$REPO_DIR/data/iot/inbound"
cd "$REPO_DIR"

python - <<'PY'
import json, random, csv, os
from datetime import datetime, timedelta, timezone

device_count = int(os.environ.get("DEVICE_COUNT", "25"))
minutes = int(os.environ.get("MINUTES", "60"))
outlier_rate = float(os.environ.get("OUTLIER_RATE", "0.03"))
missing_ts_rate = float(os.environ.get("MISSING_TS_RATE", "0.01"))

start = datetime(2026,3,1,0,0,0,tzinfo=timezone.utc)

def make_row(device_id, ts, metric):
    if metric == "temp_c":
        unit = "C"
        value = round(20 + random.uniform(-5, 8), 2)
        if random.random() < outlier_rate:
            value = random.uniform(-60, 120)
        if random.random() < outlier_rate/2:
            unit = "F"  # wrong unit
    elif metric == "humidity_pct":
        unit = "pct"
        value = round(40 + random.uniform(-15, 25), 2)
        if random.random() < outlier_rate:
            value = random.uniform(-30, 170)
    else:
        unit = "hPa"
        value = round(1013 + random.uniform(-30, 30), 2)
        if random.random() < outlier_rate:
            value = random.uniform(100, 2000)

    ts_out = ts
    if random.random() < missing_ts_rate:
        ts_out = ""

    return {
        "device_id": device_id,
        "reading_ts": ts_out,
        "metric": metric,
        "value": round(value, 2),
        "unit": unit,
    }

rows = []
for d in range(1, device_count+1):
    device_id = f"DEV-{d:04d}"
    for m in range(minutes):
        ts = (start + timedelta(minutes=m)).strftime("%Y-%m-%dT%H:%M:%SZ")
        for metric in ("temp_c","humidity_pct","pressure_hpa"):
            rows.append(make_row(device_id, ts, metric))

csv_path = "data/iot/inbound/telemetry.csv"
json_path = "data/iot/inbound/telemetry.json"

with open(csv_path,"w",newline="",encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["device_id","reading_ts","metric","value","unit"])
    w.writeheader()
    w.writerows(rows)

with open(json_path,"w",encoding="utf-8") as f:
    json.dump(rows,f,indent=2)

print("Generated:")
print(" ", csv_path)
print(" ", json_path)
print("Rows:", len(rows))
PY
