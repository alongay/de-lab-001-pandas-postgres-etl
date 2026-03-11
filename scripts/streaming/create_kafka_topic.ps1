# create_kafka_topic.ps1
# Ensures the IoT telemetry topic exists in Kafka.

$TOPIC = "iot.telemetry.raw"
$PARTITIONS = 3
$REPLICATION = 1

Write-Host "[STATUS] Creating Kafka topic: $TOPIC..." -ForegroundColor Cyan

# Using the kafka container to run the command (Note: hyphenated name)
docker exec pde-iot-kafka kafka-topics.sh --create --if-not-exists --topic $TOPIC --partitions $PARTITIONS --replication-factor $REPLICATION --bootstrap-server localhost:9092

if ($LASTEXITCODE -eq 0) {
    Write-Host "[SUCCESS] Topic $TOPIC is ready." -ForegroundColor Green
} else {
    Write-Host "[ERROR] Failed to create topic $TOPIC." -ForegroundColor Red
    exit 1
}
