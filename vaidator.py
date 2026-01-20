def valiate_ping(data):
	if data is None:
		return False

	if data['latency'] < 0 or data['latency'] > 100:
		return False
	if data['packet_loss'] < 0 or data['packet_loss'] > 100:
		return False

	return True


