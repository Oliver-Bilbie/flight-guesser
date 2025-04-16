#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

# Check and set STAGE
if [ -z "$STAGE" ]; then
  echo "Please set the STAGE environment variable (e.g., export STAGE=dev)"
  exit 1
fi

echo "Using STAGE: $STAGE"

# Retrieve parameters from SSM Parameter Store
DEPLOY_BUCKET_NAME=$(aws ssm get-parameter --name "flight-guesser-${STAGE}-host-bucket" --with-decryption --query "Parameter.Value" --output text)
CF_DISTRIBUTION_ID=$(aws ssm get-parameter --name "flight-guesser-${STAGE}-cdn-id" --with-decryption --query "Parameter.Value" --output text)

echo "Retrieved DEPLOY_BUCKET_NAME: $DEPLOY_BUCKET_NAME"
echo "Retrieved CF_DISTRIBUTION_ID: $CF_DISTRIBUTION_ID"

# === INSTALL PHASE ===
echo "Installing pipeline dependencies..."
make install-python-deps
make install-node-deps
make install-serverless

# === PRE_BUILD PHASE ===
echo "Preparing versioning..."
VERSION=$(sed 's/.*"version": "\(.*\)".*/\1/;t;d' ./package.json)
sed -i "s/VERSION_NUMBER/$VERSION/g" ./frontend/package.json
echo "Version set to $VERSION"

# === BUILD PHASE ===
echo "Running Terraform deployment..."
make deploy-terraform STAGE=$STAGE

echo "Deploying backend..."
make deploy-backend STAGE=$STAGE

echo "Deploying frontend..."
make deploy-frontend STAGE=$STAGE DEPLOY_BUCKET_NAME=$DEPLOY_BUCKET_NAME CF_DISTRIBUTION_ID=$CF_DISTRIBUTION_ID

# === POST_BUILD PHASE ===
echo "Running post-build steps..."
# Revert version number change
git checkout HEAD -- frontend/package.json

BUILD_EXIT_CODE=$?

if [ "$STAGE" == "prd" ]; then
  if [ "$BUILD_EXIT_CODE" -ne 0 ]; then
    badge_status="failing"
    badge_colour="red"
  else
    badge_status="passing"
    badge_colour="green"
  fi

  curl -s "https://img.shields.io/badge/build-$badge_status-$badge_colour.svg" -o "build-status.svg"
  aws s3 cp "build-status.svg" "s3://flight-guesser-prd/build-status.svg" --cache-control no-cache
fi

echo "Build script completed."
