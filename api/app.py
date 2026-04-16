from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

# DB Connection
conn = psycopg2.connect(
    dbname="rides",
    user="admin",
    password="admin",
    host="database",
    port="5432"
)

@app.route('/api/zones/live', methods=['GET'])
def get_zones():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM zone_stats;")
    rows = cursor.fetchall()

    zones = []
    for row in rows:
        zones.append({
            "city_zone": row[0],
            "active_drivers": row[1],
            "pending_requests": row[2],
            "surge_multiplier": float(row[3]),
            "last_updated": row[4].isoformat()
        })

    return jsonify({"zones": zones}), 200


@app.route('/api/alerts/recent', methods=['GET'])
def get_alerts():
    cursor = conn.cursor()
    cursor.execute("""
        SELECT alert_id, city_zone, surge_multiplier, timestamp
        FROM surge_alerts
        ORDER BY timestamp DESC
        LIMIT 20;
    """)
    rows = cursor.fetchall()

    alerts = []
    for row in rows:
        alerts.append({
            "alert_id": row[0],
            "city_zone": row[1],
            "surge_multiplier": float(row[2]),
            "timestamp": row[3].isoformat()
        })

    return jsonify({"alerts": alerts}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)