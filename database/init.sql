-- Create zone_stats table
CREATE TABLE IF NOT EXISTS zone_stats (
    city_zone VARCHAR PRIMARY KEY,
    active_drivers INTEGER NOT NULL,
    pending_requests INTEGER NOT NULL,
    surge_multiplier FLOAT NOT NULL,
    last_updated TIMESTAMP NOT NULL
);

-- Create surge_alerts table
CREATE TABLE IF NOT EXISTS surge_alerts (
    alert_id VARCHAR PRIMARY KEY,
    city_zone VARCHAR NOT NULL,
    surge_multiplier FLOAT NOT NULL,
    timestamp TIMESTAMP NOT NULL
);

