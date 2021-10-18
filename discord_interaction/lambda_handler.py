import os
import boto3

def handler(event, context):

    response = unauthorized_request(event)
    if response:
        return response

    return {
        "statusCode": 200,
    }

def unauthorized_request(event) -> dict:
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

    #todo implement authentication
    public_key = os.environ['DISCORD_PUBLIC_KEY']


    return {
        'statusCode': 401
    }
