from dataclasses import dataclass, asdict

import boto3

client = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')
GUILD_TABLE_NAME = 'dti_guilds'
GUILD_PRIMARY_KEY = 'guild_id'
USER_TABLE_NAME = 'dti_users'
USER_PRIMARY_KEY = 'discord_user_id'


@dataclass
class Table:
    table_name: str
    primary_key: str


@dataclass
class Guild:
    guild_id: int
    board_id: str
    list_id: str


@dataclass
class User:
    discord_user_id: int
    trello_id: str
    access_token: str = "token"
    subscribed: bool = True




def create_table(table: Table):
    client.create_table(
        AttributeDefinitions=[
            {
                'AttributeName': table.primary_key,
                'AttributeType': 'N'
            }
        ],
        KeySchema=[
            {
                'AttributeName': table.primary_key,
                'KeyType': 'HASH'
            }
        ],
        TableName=table.table_name,
        BillingMode='PAY_PER_REQUEST'
    )


def add_user(user: User):
    table = client.Table(USER_TABLE_NAME)
    table.put_item(
        Item=asdict(user)
    )

def add_guild(guild: Guild):
    table = client.Table(GUILD_TABLE_NAME)
    client.put_item(
        Item=asdict(guild)
    )

def init_db():

    existing_tables = client.tables.all()

    for table in existing_tables:
        table.delete()

    create_table(Table(GUILD_TABLE_NAME, GUILD_PRIMARY_KEY))
    create_table(Table(USER_TABLE_NAME, USER_PRIMARY_KEY))
