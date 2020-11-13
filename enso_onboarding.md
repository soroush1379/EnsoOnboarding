## Enso Connect onboarding challenge

One of enso's key features is our unified inbox, which combines messages across email, SMS, airbnb &whatsapp. For this challenge, you are tasked with "integrating" our messages database with Airbnb's messaging API.

### Given
* You are given a mock version of the the airbnb API client, which returns an array of airbnb threads at different time steps. Each thread corresponds to a conversation with a guest (just like in any messenger application) and contains an array of messages. Make any assumptions you need to about the schema of each thread.
 ```python
class AirbnbClient:  
	def __init__(self):  
		pass
	def get_messages(self, step=1):  
		return threads
```
* You are also given the minimal schema of our message database object, which you may expand on.
```json
message = {
	"guest_id": str,
	"sent": int # milliseconds timestamp
	"message": str
	"user": Literal['guest', 'owner']
	"channel": Literal['airbnb','SMS','email','whatsapp']
	...
}
```
### Challenge Specs
You will be building a polling function, `SyncAirbnb`, that synchronizes the airbnb threads with our internal store of messages.

```python
class SyncAirbnb:
	def __init__(self, ...):
		self.messages = ...

	def __call__(self):
		...
```
Complete as many levels as you can.

* Level 1: Using SyncAirbnb's messages attribute as your database, synchronize the messages at the first timestep. In other words, call `AirbnbClient.get_messages()` , parse the response, and push all the messages into `SyncAirbnb.messages`.

* Level 2: Modify SyncAirbnb messages to synchronize the messages at the second timestep. In other words, push in any new messages to `SyncAirbnb.messages` that were not present in timestep 1.

* Level 3: Modify `SyncAirbnb` to save & query to a dynamoDB table, replacing `SyncAirbnb.messages` as your database. You will need an AWS account & boto3 configured on your machine for this. Use `guest_id` as primary key and `sent` as sort key.

* Level 4: Write a unit test for `SyncAirbnb`. Note that you cannot call the airbnb or dynamodb clients in your test (since these are live), so you will need to mock their responses, either manually or by copying/modifying the contents of `threads.json`. Inject those dependancies!
<!--stackedit_data:
eyJoaXN0b3J5IjpbNTkzNjcwMzRdfQ==
-->
