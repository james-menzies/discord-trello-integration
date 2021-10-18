import boto3

client = boto3.client('dynamodb', endpoint_url='http://localhost:8000')

existing_tables = client.list_tables()['TableNames']

for table in existing_tables:
    client.delete_table(TableName=table)


client.create_table(
    AttributeDefinitions=[
        {
           'AttributeName': 'guild_id',
           'AttributeType': 'N'
        }
    ],
    KeySchema=[
        {
            'AttributeName': 'guild_id',
            'KeyType': 'HASH'
        }
    ],
    TableName='dti_guilds',
    BillingMode='PAY_PER_REQUEST'
)

client.create_table(
    AttributeDefinitions=[
        {
            'AttributeName': 'discord_user_id',
            'AttributeType': 'N'
        }
    ],
    KeySchema=[
        {
            'AttributeName': 'discord_user_id',
            'KeyType': 'HASH'
        }
    ],
    TableName='dti_users',
    BillingMode='PAY_PER_REQUEST'
)

