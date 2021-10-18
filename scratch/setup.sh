#!/bin/bash

curl --request POST \
  --url https://discord.com/api/v9/applications/${DISCORD_APPLICATION_ID}/commands \
  --header "Authorization: Bot ${DISCORD_BOT_TOKEN}"\
  --header 'Content-Type: application/json' \
  --data @command_payload.json