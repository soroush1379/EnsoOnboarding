from enso_onboarding import AirbnbClient
from datetime import datetime

class SyncAirbnb:
	"""
	This class parses messages received from the Airbnb API and synchronizes the airbnb threads with the internal store of messages.
	"""
	def  __init__(self):
		self.messages = []
		return


	def __call__(self, step):
		# Retrieve the messages from the Airbnb API
		client = AirbnbClient()
		threads = client.get_messages(step=step)

		# Adding the message into the internal storage
		for thread in threads:
			# Retrieving user information
			owner_ids, guest_ids, cohost_ids, booker_ids = self.__get_user_ids(thread["attachment"]["roles"])
			user_names = self.__get_user_names(thread["users"])

			for raw_message in thread["messages"]:
				# Retrieving the message from the input
				message = raw_message["message"]
				message_id = raw_message["id"]
				attachment_images = raw_message["attachment_images"]
				date = datetime.strptime(raw_message["created_at"], "%Y-%m-%dT%H:%M:%SZ")
				timestamp = int(date.timestamp() * 1000)

				owner_id = owner_ids[0]  # Only the first owner will be considered
				sender_id = raw_message["user_id"]   # The guest presumably

				message_instance = {
					"guest_id": str(sender_id),
					"owner_id": str(owner_ids[0]),      # id of the first owner
					"timestamp": timestamp,
					"message_id": str(message_id),
					"message": message,
					"attachment_images": attachment_images,
					"user": [user_names[sender_id], user_names[owner_id]],
					"channel": "airbnb",
					"date": date.strftime("%m/%d/%Y, %H:%M:%S"),
					}

				# If the message already exists, the message is not added
				if self.__message_exists(message_instance):
					continue

				# Adding the message
				self.messages += [message_instance]

		return

	def __message_exists(self, input_message):
		for message in self.messages:
			if message["message_id"] == input_message["message_id"] and message["timestamp"] == input_message["timestamp"]:
				return True

		return False

	def __get_user_names(self, users):
		"""
		This function returns the name of all users in the form of a dictionary with the user_ids being the keys. users it thread["users"] part of the airbnb api output.
		"""
		names = {}
		for user in users:
			names[user["id"]] = user["first_name"]

		return names

	def __get_user_ids(self, roles):
		"""
		This function returns the owner/guest/cohost ids. The input is roles, which is the thread["attatchment"]["roles"] part of the Airbnb API output.
		"""
		owner_ids = []
		guest_ids = []
		cohost_ids = []
		bookers_ids = []

		for role in roles:
			if role["role"] == "guest":
				guest_ids = role["user_ids"]
			if role["role"] == "owner":
				owner_ids = role["user_ids"]
			if role["role"] == "cohost":
				cohost_ids = role["user_ids"]
			if role["role"] == "booker":
				bookers_ids = role["user_ids"]

		return owner_ids, guest_ids, cohost_ids, bookers_ids


if __name__ == "__main__":
	instance = SyncAirbnb()
	instance(1)
	instance(2)
	for message in instance.messages:
		print(message)

	pass
