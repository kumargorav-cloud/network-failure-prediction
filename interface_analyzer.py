import sqlite3

def analyze_interface(interface='eth0',limit=5):
	conn=sqlite3.connect('network.db')
	cursor=conn.cursor()

	cursor.execute("""
	SELECT rx_errors, tx_errors, rx_dropped, tx_dropped
	FROM interface_stats
	WHERE interface=?
	ORDER BY timestamp DESC
	LIMIT ?
	""", (interface,limit))

	rows=cursor.fetchall()
	conn.close()


	if len(rows) < limit:
		return "Not enough data"

	rx_err=[r[0] for r in rows]
	tx_err=[r[1] for r in rows]
	drops=[r[2] + r[3] for r in rows]

	if rx_err[0] > rx_err[-1] or tx_err[0] > tx_err[-1]:
		return "Interface errors increasing"

	if drops[0] > drops[-1]:
		return "Packet drops increasing"

	return "Interface stable"
