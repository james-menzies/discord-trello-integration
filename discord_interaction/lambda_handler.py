import json
import os
from typing import Optional

import boto3
from nacl.exceptions import BadSignatureError
from nacl.signing import VerifyKey

def build_payload(body: dict, statusCode: int = 200) -> dict:
    """
    Builds an appropriate payload for the API Gateway interface.
    :param body: The dictionary object representing the payload
    that should be returned to Discord
    :param statusCode:
    :return: The payload expected by API Gateway.
    """

    # content-type header required, as it appears to cause
    # an error for Discord if not present.
    return {
        'statusCode': statusCode,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(body)
    }


def handler(event, context):

    # Verify authenticity of request
    response = unauthorized_request(event)
    if response:
        return response

    # Verify that payload is valid
    body = json.loads(event['body'])
    if 'type' not in body:
        return build_payload({}, 400)

    if body['type'] == 1:
        return build_payload({'type': 1})

    return build_payload({}, 200)




def unauthorized_request(event) -> Optional[dict]:
    """
    Checks the request to make sure that it is a valid Discord interaction.
    The conditions that must be met are:

    * Request must contain a header for the signature and timestamp of request
    * Signature must be valid.

    Discord will routinely check that this process being correctly performed, and
    will disable non-compliant bots, so it is imperatively that this function is called
    at the front of this request.
    :param event: The event object passed into the lambda function.
    :return: A return object that contains the correct payload for the API response.
    """

    DISCORD_PUBLIC_KEY = os.getenv('DISCORD_PUBLIC_KEY')

    # AWS_SAM_LOCAL is only present in the env if this function is running locally,
    # when deployed this conditional will always fail. This helps get around the
    # pain of ensuring that every single test case is signed correctly against
    # the payload of the request.
    #
    # However, if there are authentication headers present, this function will proceed
    # as normal, allowing the authentication process itself to be tested locally.
    if 'AWS_SAM_LOCAL' in os.environ and 'x-signature-timestamp' not in event['headers']:
        return

    body = event['body']

    public_key = bytes.fromhex(DISCORD_PUBLIC_KEY)
    vk = VerifyKey(public_key)

    try:
        signature = event['headers']['x-signature-ed25519']
        timestamp = event['headers']['x-signature-timestamp']
    except KeyError:
        return build_payload({}, 401)

    try:
        vk.verify(f'{timestamp}{body}'.encode(), bytes.fromhex(signature))
    except BadSignatureError:
        return build_payload({}, 401)



