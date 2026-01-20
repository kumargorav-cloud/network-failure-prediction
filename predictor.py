from trend_analyzer import get_recent_samples, analyze_trend

def predict_failure():
	samples=get_recent_samples()

	if len(samples) < 5:
		return "Not enough data"

	inc_latency,loss_events=analyze_trend(samples)

	if inc_latency and loss_events >= 2:
		return "HIGH RISH: Failure likely"
	elif inc_latency:
		return "WARNING: Network degrading"

	else:
		return "Network stable"

if __name__ == "__main__":
	print(predict_failure())
