import json
from pathlib import Path

import boto3
import botocore
import pytest


@pytest.fixture(scope="session")
def client():
    return boto3.client('lambda',
                        region_name="ap-southeast-2",
                        endpoint_url="http://127.0.0.1:3001",
                        use_ssl=False,
                        verify=False,
                        config=botocore.client.Config(
                            signature_version=botocore.UNSIGNED,
                            read_timeout=1,
                            retries={'max_attempts': 0}
                        ))


EVENTS_DIRECTORY = Path.cwd() / "events"


def invoke_lambda(client, function_name: str, event_filepath: str = None) -> dict:
    """
    Helper method to facilitate the invocation and retrieval of a lambda function.
    :param client: The client fixture passed into the test case.
    :param function_name: The name of the function that should be invoked with the client
    :param event_filepath: The filepath relative to the root event folder which contains JSON
    to be passed into the lambda function as a payload. This should ideally be generated
    by the SAM CLI.
    :return: a dict object containing the `statusCode`, `body` and optionally, `headers`
    attribute. The body attribute will not be deserialized as JSON, as that is the format
    expected by an API Gateway. When testing, it's important that `json.loads()` is called
    on the body attribute, before any further processing of the data.
    """

    if event_filepath:

        event_filepath = EVENTS_DIRECTORY / event_filepath
        with open(event_filepath, 'r') as event_file:
            response = client.invoke(FunctionName=function_name, Payload=event_file)
    else:
        response = client.invoke(FunctionName=function_name)

    data = response['Payload'].read().decode('utf-8')
    return json.loads(data)
