import sqlite3

conn = sqlite3.connect("network.db")
cursor = conn.cursor()

cursor.execute("""
SELECT timestamp,target,latency,packet_loss
FROM network_stats
ORDER BY timestamp DESC
LIMIT 5
""")

for row in cursor.fetchall():
	print(row)

conn.close()
