# !/bin/bash

set -Eeo pipefail


##### Deploy the terraform #####
cd terraform

echo "[INFO] Installing terraform using Yum"
yum install -y yum-utils
yum-config-manager --add-repo https://rpm.releases.hashicorp.com/AmazonLinux/hashicorp.repo
yum -y install terraform

# Copy the tfstate and lock file from s3 - a bit of a hack until I put together something more elegant
aws s3 cp $TF_BUCKET_PATH"terraform.tfstate" "terraform.tfstate"
aws s3 cp $TF_BUCKET_PATH".terraform.lock.hcl" ".terraform.lock.hcl"

echo "[INFO] Removing cached terraform modules"
rm -Rf .terraform/modules

echo "[INFO] Initialiasing terraform in ${BUILD_ENV} environment"
terraform init -reconfigure -backend-config="./environments/${BUILD_ENV}/backend.conf"

echo "[INFO] Validating terraform code"
terraform validate

echo "[INFO] Deploying the infrastructure in ${BUILD_ENV} environment"
terraform apply -auto-approve -var-file="./environments/${BUILD_ENV}/terraform.tfvars"

# Write the tfstate and lock file back to s3
aws s3 cp "terraform.tfstate" $TF_BUCKET_PATH"terraform.tfstate"
aws s3 cp ".terraform.lock.hcl" $TF_BUCKET_PATH".terraform.lock.hcl"

cd ..


##### Deploy the backend #####
cd backend

echo "[INFO] Installing serverless framework and required plugins"
npm install

echo "[INFO] Installing backend dependencies"
python -m pipenv install

echo "[INFO] Deploying backend to ${BUILD_ENV} environment"
pipenv requirements > requirements.txt
npx sls deploy -s ${STAGE}

cd ..


##### Deploy the frontend #####
# Set the version number in package.json from the root directory
VERSION=$(sed 's/.*"version": "\(.*\)".*/\1/;t;d' ./package.json)
sed -i 's/VERSION_NUMBER/'$VERSION'/g' ./frontend/package.json
cd frontend

echo "[INFO] Installing frontend dependencies"
yarn

echo "[INFO] Building frontend"
yarn build:${STAGE}

echo "[INFO] Writing frontend files to S3"
aws s3 cp build $DEPLOY_BUCKET_NAME --recursive

echo "[INFO] Invalidating Cloudfront cache"
aws cloudfront create-invalidation --distribution-id $CF_DISTRIBUTION_ID --paths '/*'
