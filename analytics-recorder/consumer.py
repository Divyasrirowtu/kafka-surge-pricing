import json
import time
from datetime import datetime
from kafka import KafkaConsumer
import psycopg2

# Kafka Consumer
consumer = KafkaConsumer(
    'ride-requests',
    bootstrap_servers='kafka:9092',
    group_id='analytics-recorder-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# PostgreSQL Connection
conn = psycopg2.connect(
    dbname="rides",
    user="admin",
    password="admin",
    host="database",
    port="5432"
)
cursor = conn.cursor()

# In-memory state
zone_states = {}

print("📊 Analytics Recorder started...")

last_write_time = time.time()

for message in consumer:
    event = message.value
    zone = event["city_zone"]

    active_drivers = event["active_drivers"]
    pending_requests = event["pending_requests"]

    # Calculate surge
    surge = max(1.0, pending_requests / max(1, active_drivers))

    # Update in-memory state
    zone_states[zone] = {
        "active_drivers": active_drivers,
        "pending_requests": pending_requests,
        "surge_multiplier": surge,
        "last_updated": datetime.utcnow()
    }

    current_time = time.time()

    # ⏱ Write to DB every 30 seconds
    if current_time - last_write_time >= 30:
        print("💾 Writing zone stats to database...")

        for zone, data in zone_states.items():
            cursor.execute("""
                INSERT INTO zone_stats (city_zone, active_drivers, pending_requests, surge_multiplier, last_updated)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (city_zone)
                DO UPDATE SET
                    active_drivers = EXCLUDED.active_drivers,
                    pending_requests = EXCLUDED.pending_requests,
                    surge_multiplier = EXCLUDED.surge_multiplier,
                    last_updated = EXCLUDED.last_updated;
            """, (
                zone,
                data["active_drivers"],
                data["pending_requests"],
                data["surge_multiplier"],
                data["last_updated"]
            ))

        conn.commit()
        last_write_time = current_time