import sqlite3
import datetime
from logs.alert import send_alert

DB_NAME = "network.db"
TARGET = "8.8.8.8"


def get_latest_probe():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT avg_latency, jitter, packet_loss, timeouts
    FROM probe_stats
    WHERE target = ?
    ORDER BY timestamp DESC
    LIMIT 1
    """, (TARGET,))

    row = cursor.fetchone()
    conn.close()
    return row


def get_baseline():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT baseline_latency, baseline_jitter
    FROM baseline_stats
    WHERE target = ?
    """, (TARGET,))

    row = cursor.fetchone()
    conn.close()
    return row


def classify_risk(score):
    if score >= 70:
        return "HIGH"
    elif score >= 40:
        return "MEDIUM"
    elif score >= 15:
        return "LOW"
    else:
        return "STABLE"


def calculate_risk():
    latest = get_latest_probe()
    baseline = get_baseline()

    if not latest:
        return "No probe data available"
    if not baseline:
        return "Baseline not learned yet"

    avg_latency, jitter, packet_loss, timeouts = latest
    base_latency, base_jitter = baseline

    risk = 0
    reasons = []

    # Latency deviation
    latency_dev = (avg_latency - base_latency) / base_latency
    if latency_dev > 0:
        score = min(int(latency_dev * 100), 30)
        risk += score
        reasons.append(f"Latency deviation +{int(latency_dev * 100)}%")

    # Jitter deviation
    jitter_dev = (jitter - base_jitter) / (base_jitter + 0.1)
    if jitter_dev > 0:
        score = min(int(jitter_dev * 100), 30)
        risk += score
        reasons.append("Jitter instability detected")

    # Packet loss
    if packet_loss > 0:
        score = min(packet_loss * 5, 25)
        risk += score
        reasons.append(f"Packet loss {packet_loss}%")

    # Timeouts
    if timeouts > 0:
        score = min(timeouts * 5, 15)
        risk += score
        reasons.append(f"Timeouts observed ({timeouts})")

    risk = min(risk, 100)

    return {
        "risk_score": risk,
        "severity": classify_risk(risk),
        "reasons": reasons,
        "timestamp": datetime.datetime.now().isoformat(timespec="seconds")
    }


if __name__ == "__main__":
    result = calculate_risk()

    if isinstance(result, dict):
        print(f"Network Risk: {result['risk_score']} / 100 ({result['severity']})")

        for r in result["reasons"]:
            print(f" - {r}")

        if result["severity"] in ["HIGH", "MEDIUM"]:
            send_alert(result)
    else:
        print(result)


