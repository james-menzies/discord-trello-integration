def test_valid_auth(client):

    with open('./events/discord_interaction/discord_valid_auth.json', 'r') as event_file:
        response = client.invoke(FunctionName="DiscordInteractionEndpoint", Payload=event_file)


    assert response['StatusCode'] == 200


def test_invalid_auth(client):
    with open('./events/discord_interaction/discord_invalid_auth.json', 'r') as event_file:
        response = client.invoke(FunctionName="DiscordInteractionEndpoint", Payload=event_file)

    assert response['StatusCode'] == 401

