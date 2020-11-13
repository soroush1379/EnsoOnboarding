import json

class AirbnbClient:
	def __init__(self):
		pass

	def get_messages(self, step=1):
		if step not in [1,2]:
			return False
		with open(f'threads_{step}.json') as file:
		  return json.load(file)
