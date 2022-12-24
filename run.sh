#!/bin/bash

set -e

echo "Downloading weights"
bash prepare.sh
echo "Weights are downloaded"

echo "Creating containers"
docker-compose up --build