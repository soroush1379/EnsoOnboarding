import boto3

table_name = "table_messages"

class table_messages:
    def __init__(self, verbosity=False):
        # Check if table exists, and if not, produce it
        self.client = boto3.client('dynamodb')
        self.dynamodb = boto3.resource('dynamodb')
        self.verbosity = verbosity

        table_names = self.client.list_tables()["TableNames"]
        if table_name not in table_names:
            self.create_table()

        self.table = self.dynamodb.Table(table_name)

        return

    def __remove_duplicate_keys(self, messages):
        fixed_messages = []
        keys_messages = {}

        get_key = lambda message : message["guest_id"] + "_" + str(message["timestamp"])

        for message in messages:
            key = get_key(message)
            if key not in list(keys_messages.keys()):
                keys_messages[key] = [message]
            else:
                keys_messages[key] = []

        for key in list(keys_messages.keys()):
            if len(keys_messages[key]) == 1:
                fixed_messages += [keys_messages[key][0]]

        return fixed_messages

    def add(self, messages):
        # Adds a list of message instances to the table. The input MUST be a list.

        # Messages with duplicate keys are removed. This should not be possible.
        fixed_messages = self.__remove_duplicate_keys(messages)

        if self.verbosity:
            print(f"{len(messages) - len(fixed_messages)} messages out of {len(messages)} had the same keys and ignored.")
            print(f"Adding {len(fixed_messages)} messages to the database...")
        # Batch writes the messages onto the table
        with self.table.batch_writer() as batch:
            for message in fixed_messages:
                batch.put_item(Item=message)

        if self.verbosity:
            print("Process successful.\n")

        return True

    def contains(self, message):
        # Checks if the table contains a given message
        request = self.table.get_item(
            Key = {
            "guest_id": message["guest_id"],
            "timestamp": message["timestamp"]
            }
        )

        return "Item" in list(request.keys())

    def delete_table(self):
        # Deletes the table.
        if self.verbosity:
            print("Deleting table_messages...")

        self.table.delete()
        table.wait_until_not_exists()

        if self.verbosity:
            print("Process completed.\n")

    def create_table(self):
        if self.verbosity:
            print("table_messages does not exist. Generating the table...")

        table = self.dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'guest_id',
                    'KeyType': 'HASH' # Partition Key
                },
                {
                    'AttributeName': 'timestamp',
                    'KeyType': 'RANGE' # Sort Key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'guest_id',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'timestamp',
                    'AttributeType': 'N'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5,
            }
        )

        # table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
        table.wait_until_exists()

        if self.verbosity:
            print("Table generated\n")

        return
