import sqlite3

conn = sqlite3.connect("network.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS interface_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    interface TEXT,
    rx_errors INTEGER,
    tx_errors INTEGER,
    rx_dropped INTEGER,
    tx_dropped INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS baseline_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    target TEXT UNIQUE,
    baseline_latency REAL,
    baseline_jitter REAL,
    learned_samples INTEGER,
    updated_at TEXT
)
""")
conn.commit()
conn.close()

