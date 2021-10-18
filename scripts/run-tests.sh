#!/bin/bash

# eliminate any existing processes
killall sam > /dev/null 2>&1
echo "Starting local lambda environment..."

# starts the lambda with specific key so auth can be tested
sam local start-lambda \
  --parameter-overrides \
  DiscordPublicKey=3f4a3e7651de9a0f298e189a6d55545b867c1d7505288c7a276d052c5f399298 \
  --log-file logs.txt \
   > /dev/null &

