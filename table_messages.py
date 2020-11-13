import boto3

table_name = "table_messages"

class table_messages:
    def __init__(self):
        # Check if table exists, and if not, produce it
        self.client = boto3.client('dynamodb')
        self.dynamodb = boto3.resource('dynamodb')

        table_names = self.client.list_tables()["TableNames"]
        if table_name not in table_names:
            self.create_table()

        self.table = self.dynamodb.Table(table_name)

        return

    def add(self, messages):
        print(f"Adding {len(messages)} messages to the database...")
        # Batch writes the messages onto the table
        with self.table.batch_writer() as batch:
            for message in messages:
                batch.put_item(Item=message)

        print("Process successful.\n")

        return True

    def contains(self, message):
        request = self.table.get_item(
            Key = {
            "guest_id": message["guest_id"],
            "timestamp": message["timestamp"]
            }
        )

        return "Item" in list(request.keys())

    def delete_table(self):
        print("Deleting table_messages...")
        self.table.delete()
        table.wait_until_not_exists()
        print("Process completed.\n")

    def create_table(self):
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

        print("Table generated\n")

        return
