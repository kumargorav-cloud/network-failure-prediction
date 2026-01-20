import subprocess
import sqlite3
import datetime
import re
import statistics

DB_NAME = "network.db"
TARGET = "8.8.8.8"
PING_COUNT = 10
PING_INTERVAL = "0.2"


def collect_ping_stats(target=TARGET):
    """
    Actively probes network health using ping.
    Collects latency, jitter, packet loss, and timeouts.
    """

    result = subprocess.run(
        ["ping", "-c", str(PING_COUNT), "-i", PING_INTERVAL, target],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    output = result.stdout

    rtts = []
    timeouts = 0

    for line in output.splitlines():
        if "time=" in line:
            # example: time=23.4 ms
            rtt = float(line.split("time=")[1].split()[0])
            rtts.append(rtt)
        elif "100% packet loss" in line or "Request timeout" in line:
            timeouts += 1

    # Packet loss %
    loss_match = re.search(r"(\d+)% packet loss", output)
    packet_loss = int(loss_match.group(1)) if loss_match else 100

    # Metrics
    avg_latency = statistics.mean(rtts) if rtts else None
    jitter = statistics.pstdev(rtts) if len(rtts) > 1 else 0.0

    return {
        "timestamp": datetime.datetime.now().isoformat(timespec="seconds"),
        "target": target,
        "avg_latency": avg_latency,
        "jitter": jitter,
        "packet_loss": packet_loss,
        "timeouts": timeouts
    }


def save_to_db(data):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS probe_stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        target TEXT,
        avg_latency REAL,
        jitter REAL,
        packet_loss INTEGER,
        timeouts INTEGER
    )
    """)

    cursor.execute("""
    INSERT INTO probe_stats
    (timestamp, target, avg_latency, jitter, packet_loss, timeouts)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data["timestamp"],
        data["target"],
        data["avg_latency"],
        data["jitter"],
        data["packet_loss"],
        data["timeouts"]
    ))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    stats = collect_ping_stats()
    save_to_db(stats)

