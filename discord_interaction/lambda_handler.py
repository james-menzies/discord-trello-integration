import json
import os

import boto3

def handler(event, context):

    print(os.environ['DISCORD_PUBLIC_KEY'])

    return {
        "statusCode": 200,
    }
