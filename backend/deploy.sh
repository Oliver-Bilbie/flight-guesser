#!/bin/bash

set -e

if [ -z "$STAGE" ]; then
  echo "Please set the STAGE environment variable (e.g., export STAGE=dev)"
  exit 1
fi

echo "Building backend for $STAGE environment"

# Create a fresh build directory
rm -rf ./build
mkdir -p ./build

# Zip lambda files
pushd src/service > /dev/null || exit 1
rm -rf __pycache__
zip -r ../../build/server.zip .
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
