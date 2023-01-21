# !/bin/bash

set -Eeo pipefail
trap "echo '[FAILED]' && exit 1" ERR

echo "[INFO] Installing terraform"
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://rpm.releases.hashicorp.com/AmazonLinux/hashicorp.repo
sudo yum -y install terraform

### Deploy the terraform
cd terraform
# Copy the tfstate and lock file from s3 - a bit of a hack until I get it working properly
aws s3 cp $TF_BUCKET_PATH"terraform.tfstate" "terraform.tfstate"
aws s3 cp $TF_BUCKET_PATH".terraform.lock.hcl" ".terraform.lock.hcl"
make init
make apply
# Write the tfstate and lock file back to s3
aws s3 cp "terraform.tfstate" $TF_BUCKET_PATH"terraform.tfstate"
aws s3 cp ".terraform.lock.hcl" $TF_BUCKET_PATH".terraform.lock.hcl"
cd ..

echo "[INFO] Installing serverless framework and required plugins"
cd backend
npm install
cd ..

echo "[INFO] Installing required Python dependencies"
cd backend
pipenv install
cd ..

### Deploy the backend using serverless framework
make deploy-backend

### Build and deploy the frontend to S3
# Set the version number in package.json from the root directory
VERSION=$(sed 's/.*"version": "\(.*\)".*/\1/;t;d' ./package.json)
sed -i 's/VERSION_NUMBER/'$VERSION'/g' ./frontend/package.json
# Build production UI
make build-frontend
# Copy the files to S3
aws s3 cp frontend/build $DEPLOY_BUCKET_NAME --recursive
# Invalidate the Cloudfront cache so that the changes may take effect
aws cloudfront create-invalidation --distribution-id $CF_DISTRIBUTION_ID --paths '/*'
