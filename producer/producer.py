import json
import time
import uuid
import random
from datetime import datetime
from kafka import KafkaProducer

# Connect to Kafka
producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    key_serializer=lambda k: k.encode('utf-8')
)

city_zones = [
    "downtown",
    "airport",
    "suburbs-north",
    "suburbs-south",
    "business-district",
    "stadium-complex"
]

def generate_event(zone):
    return {
        "event_id": str(uuid.uuid4()),
        "city_zone": zone,
        "timestamp": datetime.utcnow().isoformat(),
        "active_drivers": random.randint(0, 50),
        "pending_requests": random.randint(0, 100)
    }

print("🚀 Producer started...")

while True:
    for zone in city_zones:
        event = generate_event(zone)

        # 🔥 KEY = city_zone (VERY IMPORTANT)
        producer.send(
            topic='ride-requests',
            key=zone,
            value=event
        )

        print(f"Sent event: {event}")

    time.sleep(1)