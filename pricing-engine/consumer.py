import json
import uuid
from datetime import datetime
from kafka import KafkaConsumer, KafkaProducer
import psycopg2

# Kafka Consumer
consumer = KafkaConsumer(
    'ride-requests',
    bootstrap_servers='kafka:9092',
    group_id='pricing-engine-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Kafka Producer (for alerts)
producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
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

print("🚀 Pricing Engine Consumer started...")

for message in consumer:
    event = message.value

    active_drivers = event["active_drivers"]
    pending_requests = event["pending_requests"]

    # 🔥 Surge Formula
    surge = max(1.0, pending_requests / max(1, active_drivers))

    print(f"Zone: {event['city_zone']} | Surge: {surge}")

    if surge > 2.0:
        alert = {
            "alert_id": str(uuid.uuid4()),
            "city_zone": event["city_zone"],
            "surge_multiplier": surge,
            "timestamp": datetime.utcnow().isoformat()
        }

        # Send to Kafka topic
        producer.send("surge-alerts", value=alert)

        # Save to DB
        cursor.execute("""
            INSERT INTO surge_alerts (alert_id, city_zone, surge_multiplier, timestamp)
            VALUES (%s, %s, %s, %s)
        """, (
            alert["alert_id"],
            alert["city_zone"],
            alert["surge_multiplier"],
            alert["timestamp"]
        ))

        conn.commit()

        print(f"🚨 Alert generated: {alert}")