#!/bin/bash

set -e

if [ -z "$STAGE" ]; then
  echo "Please set the STAGE environment variable (e.g., export STAGE=dev)"
  exit 1
fi

echo "Building backend for $STAGE environment"

# Create a fresh build directory
rm -rf ./build
mkdir -p ./build ./build/singleplayer_src ./build/multiplayer_src

# Build singleplayer server
cp -r ./src/service/* ./build/singleplayer_src
pushd ./build/singleplayer_src > /dev/null || exit 1
rm -rf ./multiplayer_server.py ./multiplayer_helpers ./__pycache__
zip -r ../singleplayer_server.zip .
popd > /dev/null

# Build multiplayer server
cp -r ./src/service/* ./build/multiplayer_src
pushd ./build/multiplayer_src > /dev/null || exit 1
rm -rf ./singleplayer_server.py ./__pycache__
zip -r ../multiplayer_server.zip .
popd > /dev/null

# Deploy Terraform
echo "Running Terraform deployment"
pushd ../terraform > /dev/null || exit 1

ENV_VAR_FILE="./environments/${STAGE}/terraform.tfvars"
BACKEND_CONF="./environments/${STAGE}/backend.conf"

# terraform init -upgrade -reconfigure -backend-config=${BACKEND_CONF}
terraform validate
terraform apply -var-file=${ENV_VAR_FILE}

CLOUDFRONT_DIST=$(terraform output -raw cloudfront_distribution)
HOST_BUCKET=$(terraform output -raw host_bucket)
SINGLEPLAYER_ENDPOINT=$(terraform output -raw singleplayer_endpoint)

popd > /dev/null


echo "Build script completed."
