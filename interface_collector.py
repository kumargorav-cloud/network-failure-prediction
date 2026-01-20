import subprocess
import sqlite3
import datetime

INTERFACE = "wifi0"

def collect_interface_stats():
	result=subprocess.run(['ip','-s','link','show',INTERFACE],stdout=subprocess.PIPE,text=True)

	line=result.stdout.splitlines()
	rx=lines[3].split()
	tx=lines[5].split()

	return {
		"timestamp":datetime.datetime.now.isoformat(timespec='seconds'),
		"interface":INTERFACE,
		"rx_errors":int(rx[2]),
		"rx_dropped":int(rx[3]),
		"tx_errors":int(tx[2]),
		"tx_dropped":int(tx[3])
		}

def save(stats):
	conn=sqlite3.connect('network.db')

