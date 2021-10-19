#!/bin/bash

# eliminate any existing processes
echo "Removing dangling processes..."
{
killall sam > /dev/null
docker rm -f `docker ps -q`
} > /dev/null 2>&1

# rebuild any changes that have occurred since last suite run
echo "Rebuilding codebase..."
sam build > /dev/null 2>&1

# restart the local db instance
echo "Rebuilding local DynamoDB..."
{
docker-compose down
docker-compose up -d
}

# starts the lambda with specific key so auth can be tested
echo "Starting local lambda environment..."
sam local start-lambda \
  --docker-network trello-network \
  --warm-containers EAGER \
  --parameter-overrides \
  DiscordPublicKey=3f4a3e7651de9a0f298e189a6d55545b867c1d7505288c7a276d052c5f399298 \
  > /dev/null 2>&1 &

sleep 2

echo "Ready to run test suite"

