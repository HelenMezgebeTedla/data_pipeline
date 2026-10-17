import json
import logging
import sqlite3
import time
import urllib.request
from datetime import datetime, timezone

API_URL = "https://jsonplaceholder.typicode.com/users"
DB_PATH = "warehouse.db"
TABLE = "users"
MAX_RETRIES = 3

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.FileHandler("pipeline.log"), logging.StreamHandler()],
)
log = logging.getLogger("pipeline")


def fetch_users():
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            with urllib.request.urlopen(API_URL, timeout=10) as resp:
                data = json.loads(resp.read().decode())
            log.info("Fetched %d records from API", len(data))
            return data
        except Exception as exc:
            log.warning("Attempt %d failed: %s", attempt, exc)
            time.sleep(2 * attempt)
    raise RuntimeError("Failed to fetch data after retries")


def init_db(conn):
    conn.execute(
        f"""CREATE TABLE IF NOT EXISTS {TABLE} (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT,
            city TEXT,
            loaded_at TEXT NOT NULL
        )"""
    )
    conn.commit()


def upsert(conn, records):
    now = datetime.now(timezone.utc).isoformat()
    for r in records:
        conn.execute(
            f"""INSERT INTO {TABLE} (id, name, email, city, loaded_at)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    name=excluded.name, email=excluded.email,
                    city=excluded.city, loaded_at=excluded.loaded_at""",
            (r["id"], r["name"], r.get("email"), r.get("address", {}).get("city"), now),
        )
    conn.commit()
    log.info("Upserted %d records", len(records))


def main():
    log.info("Pipeline started")
    records = fetch_users()
    conn = sqlite3.connect(DB_PATH)
    try:
        init_db(conn)
        upsert(conn, records)
    finally:
        conn.close()
    log.info("Pipeline finished successfully")


if __name__ == "__main__":
    main()
