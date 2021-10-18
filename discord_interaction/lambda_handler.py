import os
from typing import Optional

import boto3
from nacl.exceptions import BadSignatureError
from nacl.signing import VerifyKey


def handler(event, context):

    response = unauthorized_request(event)

    if response:
        return response


    return {
        "statusCode": 200,
    }


def unauthorized_request(event) -> Optional[dict]:
    """
    Checks the request to make sure that it is a valid Discord interaction.
    The conditions that must be met are:

    * Request body must have a 'type' attribute
    * Request must contain a header for the signature and timestamp of request
    * Signature must be valid.

    Discord will routinely check that this process being correctly performed, and
    will disable non-compliant bots, so it is imperatively that this function is called
    at the front of this request.
    :param event: The event object passed into the lambda function.
    :return: A return object that contains the correct payload for the API response.
    """
    UNAUTHORIZED = {
        'statusCode': 401
    }

    DISCORD_PUBLIC_KEY = os.getenv('DISCORD_PUBLIC_KEY')

    if 'AWS_SAM_LOCAL' in os.environ and 'x-signature-timestamp' not in event['headers']:
        return

    body = event['body']
    public_key = bytes.fromhex(DISCORD_PUBLIC_KEY)

    vk = VerifyKey(public_key)
    try:
        signature = event['headers']['x-signature-ed25519']
        timestamp = event['headers']['x-signature-timestamp']
    except KeyError:
        return UNAUTHORIZED

    try:
        vk.verify(f'{timestamp}{body}'.encode(), bytes.fromhex(signature))
    except BadSignatureError:
        return UNAUTHORIZED


