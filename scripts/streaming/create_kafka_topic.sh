#!/usr/bin/env bash
# create_kafka_topic.sh
# Ensures the IoT telemetry topic exists in Kafka.

TOPIC="iot.telemetry.raw"
PARTITIONS=3
REPLICATION=1

echo "[STATUS] Creating Kafka topic: $TOPIC..."

docker exec pde-iot-kafka kafka-topics.sh \
  --create --if-not-exists \
  --topic "$TOPIC" \
  --partitions "$PARTITIONS" \
  --replication-factor "$REPLICATION" \
  --bootstrap-server localhost:9092

if [ $? -eq 0 ]; then
    echo "[SUCCESS] Topic $TOPIC is ready."
else
    echo "[ERROR] Failed to create topic $TOPIC."
    exit 1
fi
