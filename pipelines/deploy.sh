!/bin/bash

set -Eeo pipefail
trap "echo 'fail' && exit 1" ERR

echo "[INFO] Installing terraform"
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://rpm.releases.hashicorp.com/AmazonLinux/hashicorp.repo
sudo yum -y install terraform

# Deploy the terraform
cd terraform
make init
make destroy
make apply
cd ..

echo "[INFO] Installing serverless framework and required plugins"
npm install -g serverless
cd backend
npm install
cd ..

# Deploy the backend using serverless framework
make deploy-backend

# Build and deploy the frontend to S3
make build-frontend
if [ $STAGE == "prd" ]; then
    BUCKET_NAME="s3://oliver-bilbie.co.uk"
else
    BUCKET_NAME="s3://dev.oliver-bilbie.co.uk"
fi
aws s3 cp --recursive frontend/build/* $BUCKET_NAME
