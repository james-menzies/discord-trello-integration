import json

from tests.conftest import invoke_lambda


def test_valid_auth(client):
    response = invoke_lambda(client, "DiscordInteractionEndpoint", "discord_interaction_valid_auth.json")
    assert response['statusCode'] == 200
    body = json.loads(response['body'])

    assert body['type'] == 1


def test_invalid_auth(client):

    response = invoke_lambda(client, "DiscordInteractionEndpoint", "discord_interaction_invalid_auth.json")
    assert response['statusCode'] == 401



