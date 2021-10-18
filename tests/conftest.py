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
