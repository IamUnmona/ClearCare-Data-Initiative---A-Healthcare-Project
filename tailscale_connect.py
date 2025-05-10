import psycopg2

# === CONFIGURATION ===
DB_CONFIG = {
    "host": "100.65.144.13",       # Your Tailscale IP
    "port": 5433,                # Docker PostgreSQL port
    "database": "healthcare",
    "user": "postgres",
    "password": "postgres"
}

def test_connection_and_query():
    try:
        # Connect to the database
        conn = psycopg2.connect(**DB_CONFIG)
        print("✅ Connected to remote PostgreSQL via Tailscale!")

        # Run a query
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM hospital;")
        result = cur.fetchone()[0]
        print("🏥 Total hospitals in database:", result)

        # Clean up
        cur.close()
        conn.close()
    except Exception as e:
        print("❌ Connection failed:", e)

if __name__ == "__main__":
    test_connection_and_query()
