import psycopg2

DB_CONFIG = {
    "dbname": "mydatabase",
    "user": "myuser",
    "password": "mypassword",
    "host": "localhost",
    "port": "5432"
}

schema_sql = """
CREATE TABLE IF NOT EXISTS provinces (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    area_sq_km NUMERIC(10, 2),
    min_temp_c NUMERIC(4, 1),
    max_temp_c NUMERIC(4, 1),
    avg_rainfall_mm NUMERIC(10, 2),
    has_drought_risk BOOLEAN DEFAULT FALSE,
    has_tropical_storm_risk BOOLEAN DEFAULT FALSE,
    has_flood_inundation_risk BOOLEAN DEFAULT FALSE,
    population BIGINT,
    population_year INT,
    population_density_per_sq_km NUMERIC(10, 2)
);

CREATE TABLE IF NOT EXISTS province_roads (
    id SERIAL PRIMARY KEY,
    province_id INT REFERENCES provinces(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    length_km NUMERIC(10, 2)
);

CREATE TABLE IF NOT EXISTS province_railways (
    id SERIAL PRIMARY KEY,
    province_id INT REFERENCES provinces(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    length_km NUMERIC(10, 2)
);

CREATE TABLE IF NOT EXISTS province_seaports (
    id SERIAL PRIMARY KEY,
    province_id INT REFERENCES provinces(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    port_type VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS province_land_use (
    id SERIAL PRIMARY KEY,
    province_id INT REFERENCES provinces(id) ON DELETE CASCADE,
    purpose VARCHAR(100) NOT NULL,
    area_ha NUMERIC(12, 2),
    details TEXT
);
"""

try:
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute(schema_sql)
    conn.commit()
    print("Tables created successfully!")
except Exception as e:
    print(f"Error executing script: {e}")
finally:
    if 'cursor' in locals(): cursor.close()
    if 'conn' in locals(): conn.close()