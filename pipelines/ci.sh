!/bin/bash

set -Eeo pipefail
trap "echo '[FAILED]' && exit 1" ERR

# Evaluate S3 bucket addresses based on the build environment
if [ $STAGE == "prd" ]; then
    DEPLOY_BUCKET_NAME="s3://flight-guesser.net"
    TF_BUCKET_PATH="s3://terraform-state-yyq3vrfhye7d/flight-guesser/prd/"
elif [ $STAGE == "dev" ]; then
    DEPLOY_BUCKET_NAME="s3://dev.flight-guesser.net"
    TF_BUCKET_PATH="s3://terraform-state-yyq3vrfhye7d/flight-guesser/dev/"
else
    echo "[ERROR] Invalid Stage: "$STAGE
    exit 1
fi

echo "[INFO] Installing terraform"
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://rpm.releases.hashicorp.com/AmazonLinux/hashicorp.repo
sudo yum -y install terraform

# Deploy the terraform
cd terraform
aws s3 cp $TF_BUCKET_PATH"terraform.tfstate" "terraform.tfstate"
aws s3 cp $TF_BUCKET_PATH".terraform.loc.hcl" ".terraform.loc.hcl"
make init
make apply
aws s3 cp "terraform.tfstate" $TF_BUCKET_PATH"terraform.tfstate"
aws s3 cp ".terraform.loc.hcl" $TF_BUCKET_PATH".terraform.loc.hcl"
cd ..

echo "[INFO] Installing serverless framework and required plugins"
cd backend
npm install
cd ..

# Deploy the backend using serverless framework
make deploy-backend

# Build and deploy the frontend to S3
make build-frontend
aws s3 cp frontend/build $DEPLOY_BUCKET_NAME --recursive
