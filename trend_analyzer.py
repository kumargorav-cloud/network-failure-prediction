import sqlite3

def get_recent_samples(target='8.8.8.8',limit=10):
	conn=sqlite3.connect('network.db')
	cursor=conn.cursor()

	cursor.execute("""
	SELECT latency, packet_loss
	FROM network_stats
	WHERE target=?
	ORDER BY timestamp ASC
	LIMIT ?
	""", (target,limit))

	rows = cursor.fetchall()
	conn.close()
	return rows

def analyze_trend(samples):
	latencies=[s[0] for s in samples]
	losses=[s[1] for s in samples]
	increasing_latency = all(
		latencies[i] <= latencies[i+1]
		for i in range(len(latencies)-1)
	)
	loss_events=sum(1 for l in losses if l > 0)
	return increasing_latency, loss_events
