# 🚀 Kafka-Based Ride Surge Pricing Engine

## 📌 Overview
This project implements a **real-time event-driven surge pricing engine** using **Apache Kafka**. It simulates ride demand and dynamically calculates surge pricing similar to modern ride-hailing platforms.

The system processes streaming data, performs real-time analytics, and exposes results via REST APIs.

---

## 🏗️ Architecture

### Components:
- **Producer** → Generates ride request events
- **Kafka** → Event streaming platform
- **Pricing Engine Consumer** → Calculates surge & generates alerts
- **Analytics Recorder Consumer** → Aggregates zone stats
- **PostgreSQL Database** → Stores processed data
- **REST API** → Exposes data to users

---

## 🔄 Data Flow

1. Producer sends ride events → `ride-requests` topic  
2. Pricing Engine:
   - Calculates surge multiplier  
   - Sends alerts → `surge-alerts` topic  
   - Stores alerts in DB  
3. Analytics Recorder:
   - Maintains zone stats  
   - Writes to DB every 30 seconds  
4. API reads from DB and returns data  

---

## 📂 Project Structure
kafka-surge-pricing/
│
├── docker-compose.yml
├── .env.example
├── README.md
├── DECISIONS.md
│
├── producer/
├── pricing-engine/
├── analytics-recorder/
├── api/
├── database/
└── scripts/


---

## ⚙️ Setup Instructions

### 🔹 Prerequisites
- Docker
- Docker Compose
- VS Code (optional)

---

### 🔹 Run the Project

```bash
docker-compose down -v
docker-compose up --build

🌐 API Endpoints
1. Get Live Zone Stats
GET /api/zones/live

Response:
{
  "zones": [
    {
      "city_zone": "downtown",
      "active_drivers": 10,
      "pending_requests": 20,
      "surge_multiplier": 2.0,
      "last_updated": "timestamp"
    }
  ]
}

2. Get Recent Surge Alerts
GET /api/alerts/recent

Response:

{
  "alerts": [
    {
      "alert_id": "uuid",
      "city_zone": "airport",
      "surge_multiplier": 2.5,
      "timestamp": "timestamp"
    }
  ]
}

🔥 Key Features
Real-time event streaming using Kafka
Key-based partitioning (city_zone)
Parallel processing using consumer groups
Surge pricing calculation logic
Database persistence with PostgreSQL
REST API for data access
Fully containerized using Docker
📊 Kafka Topics
Topic	Partitions	Description
ride-requests	6	Ride events
surge-alerts	Default	Surge alerts
🧠 Surge Formula
surge = max(1.0, pending_requests / max(1, active_drivers))
🧪 Testing
System auto-generates events
API endpoints can be tested using:
Browser
Postman
curl
📌 Notes
Uses city_zone as message key for correct partitioning
Ensures ordering per zone
Supports horizontal scalability
🏁 Conclusion

This project demonstrates a scalable, fault-tolerant, event-driven architecture using Apache Kafka, similar to real-world ride-hailing platforms.