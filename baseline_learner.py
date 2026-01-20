import sqlite3
import statistics
import datetime

DB_NAME="network.db"
TARGET='8.8.8.8'
MIN_SAMPLES=20

def learn_baseline():
	conn=sqlite3.connect(DB_NAME)
	cursor=conn.cursor()

	cursor.execute("""
	SELECT avg_latency, jitter
	FROM probe_stats
	WHERE target=?
	  AND avg_latency IS NOT NULL
	""", (TARGET,))

	rows=cursor.fetchall()

	if len(rows) < MIN_SAMPLES:
		conn.close()

		return f"Not enough data to learn baseline ({len(rows)}/{MIN_SAMPLES})"
	latencies=[r[0] for r in rows]
	jitters=[r[1] for r in rows]

	baseline_latency=statistics.median(latencies)
	baseline_jitter=statistics.median(jitters)

	cursor.execute("""
	INSERT INTO baseline_stats
	(target, baseline_latency, baseline_jitter, learned_samples, updated_at)
	VALUES (?,?,?,?,?)
	ON CONFLICT(target) DO UPDATE SET
	    baseline_latency=excluded.baseline_latency,
	    baseline_jitter=excluded.baseline_jitter,
	    learned_samples=excluded.learned_samples,
	    updated_at=excluded.updated_at
	""",(
	    TARGET,
	    baseline_latency,
	    baseline_jitter,
	    len(rows),
	    datetime.datetime.now().isoformat(timespec='seconds')
	))

	conn.commit()
	conn.close()

	return "Baseline learned successfully"

if __name__ == "__main__":
	print(learn_baseline())
