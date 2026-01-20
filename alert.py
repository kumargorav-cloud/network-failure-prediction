import datetime

LOG_FILE="logs/alerts.log"

def send_alert(risk_result):
	timestamp=datetime.datetime.now().isoformat(timespec='seconds')

	message=(
		f"[{timestamp}]"
		f"RISK={risk_result['risk_score']}"
		f"SEVERITY={risk_result['severity']}"
		f"REASONS={', '.join(risk_result['reasons'])}\n"

		)

	#write to alert log
	with open(LOG_FILE, "a") as f:
		f.write(message)

	#console alert (simple but effective)
	print("ALERT TRIGGERED")
	print(message)
