#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

# Check and set STAGE
if [ -z "$STAGE" ]; then
  echo "[ERROR] Please set the STAGE environment variable (e.g, export STAGE=dev)"
  exit 1
fi
echo "[INFO] Deploying to stage: $STAGE"


echo "[INFO] Building the backend..."
pushd ./backend > /dev/null || exit 1

# Create a fresh build directory
rm -rf ./build
mkdir -p ./build ./build/singleplayer_src ./build/multiplayer_src

# Build singleplayer server
cp -r ./src/* ./build/singleplayer_src
pushd ./build/singleplayer_src > /dev/null || exit 1
rm -rf ./multiplayer_server.py ./multiplayer_helpers ./__pycache__
# Spoof the timestamps so that the zip file is deterministic.
# This prevent terraform from replacing the files unless they change.
TZ=UTC find . -exec touch --no-dereference -a -m -t 198002010000.00 {} +
TZ=UTC zip -q --move --recurse-paths --symlinks -X ../singleplayer_server.zip .
TZ=UTC touch -a -m -t 198002010000.00 ../singleplayer_server.zip
popd > /dev/null

# Build multiplayer server
cp -r ./src/* ./build/multiplayer_src
pushd ./build/multiplayer_src > /dev/null || exit 1
rm -rf ./singleplayer_server.py ./__pycache__
# Spoof the timestamps so that the zip file is deterministic.
# This prevent terraform from replacing the files unless they change.
TZ=UTC find . -exec touch --no-dereference -a -m -t 198002010000.00 {} +
TZ=UTC zip -q --move --recurse-paths --symlinks -X ../multiplayer_server.zip .
TZ=UTC touch -a -m -t 198002010000.00 ../multiplayer_server.zip
popd > /dev/null

echo "[INFO] Deploying the backend..."
pushd ../terraform > /dev/null || exit 1
terraform init -upgrade -reconfigure -backend-config="./environments/${STAGE}/backend.conf"
terraform validate
terraform apply -var-file="./environments/${STAGE}/terraform.tfvars"
CLOUDFRONT_DIST=$(terraform output -raw cloudfront_distribution)
BUCKET_NAME=$(terraform output -raw bucket_name)
BUCKET_ENDPOINT=$(terraform output -raw bucket_endpoint)
SINGLEPLAYER_ENDPOINT=$(terraform output -raw singleplayer_endpoint)
MULTIPLAYER_ENDPOINT=$(terraform output -raw multiplayer_endpoint)
popd > /dev/null

echo "[INFO] Backend deployed successfully"
popd > /dev/null


echo "[INFO] Building the frontend..."
pushd ./frontend > /dev/null || exit 1
cp ../CHANGELOG.md ./src/assets/CHANGELOG.md
sed -i "s&BUCKET_ENDPOINT_PLACEHOLDER&${BUCKET_ENDPOINT}&g" ./src/utils/endpoints.ts
sed -i "s&SINGLEPLAYER_ENDPOINT_PLACEHOLDER&${SINGLEPLAYER_ENDPOINT}&g" ./src/utils/endpoints.ts
sed -i "s&MULTIPLAYER_ENDPOINT_PLACEHOLDER&${MULTIPLAYER_ENDPOINT}&g" ./src/utils/endpoints.ts

npm run build

echo "[INFO] Syncing files to S3..."
aws s3 sync ./dist "s3://${BUCKET_NAME}"

echo "[INFO] Resetting CDN cache..."
aws cloudfront create-invalidation --distribution-id $CLOUDFRONT_DIST --paths "/*"

echo "[INFO] Frontend deployed successfully"
popd > /dev/null


echo "[INFO] Deployment completed"
