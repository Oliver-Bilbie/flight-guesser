set -Eeo pipefail


##### Get parameters based on environment. This will be moved to SSM in the next update.
if [ $STAGE == "prd" ]; then
    DEPLOY_BUCKET_NAME="s3://flight-guesser.net"
    TF_BUCKET_PATH="s3://terraform-state-yyq3vrfhye7d/flight-guesser/prd/"
    CF_DISTRIBUTION_ID="E2G3H6KPNGL3QZ"
elif [ $STAGE == "dev" ]; then
    DEPLOY_BUCKET_NAME="s3://dev.flight-guesser.net"
    TF_BUCKET_PATH="s3://terraform-state-yyq3vrfhye7d/flight-guesser/dev/"
    CF_DISTRIBUTION_ID="E7XC4KS1I2NH8"
else
    echo "[ERROR] Invalid deployment stage ($STAGE)"
    exit 1
fi


##### Deploy the terraform #####
cd terraform

echo "[INFO] Installing terraform using Yum"
yum install -y yum-utils
yum-config-manager --add-repo https://rpm.releases.hashicorp.com/AmazonLinux/hashicorp.repo
yum -y install terraform

echo "[INFO] Initialiasing terraform in ${BUILD_ENV} environment"
terraform init -reconfigure -backend-config="./environments/${BUILD_ENV}/backend.conf"

echo "[INFO] Validating terraform code"
terraform validate

echo "[INFO] Deploying the infrastructure in ${BUILD_ENV} environment"
terraform apply -auto-approve -var-file="./environments/${BUILD_ENV}/terraform.tfvars"

cd ..


##### Deploy the backend #####
cd backend

echo "[INFO] Installing serverless framework and required plugins"
npm install

echo "[INFO] Installing backend dependencies"
python -m pipenv install

echo "[INFO] Deploying backend to ${BUILD_ENV} environment"
pipenv requirements > requirements.txt
npx sls deploy -s $STAGE

cd ..


##### Deploy the frontend #####
# Set the version number in package.json from the root directory
VERSION=$(sed 's/.*"version": "\(.*\)".*/\1/;t;d' ./package.json)
sed -i 's/VERSION_NUMBER/'$VERSION'/g' ./frontend/package.json
cd frontend

echo "[INFO] Installing frontend dependencies"
yarn --prod

echo "[INFO] Building frontend"
yarn build:$STAGE

echo "[INFO] Writing frontend files to S3"
aws s3 cp build $DEPLOY_BUCKET_NAME --recursive

echo "[INFO] Invalidating Cloudfront cache"
aws cloudfront create-invalidation --distribution-id $CF_DISTRIBUTION_ID --paths '/*'
