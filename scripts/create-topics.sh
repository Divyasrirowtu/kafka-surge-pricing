#!/bin/bash

echo "Creating Kafka topics..."

kafka-topics.sh \
--create \
--topic ride-requests \
--bootstrap-server kafka:9092 \
--partitions 6 \
--replication-factor 1

kafka-topics.sh \
--create \
--topic surge-alerts \
--bootstrap-server kafka:9092 \
--replication-factor 1

echo "Topics created successfully!"