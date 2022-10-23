!/bin/bash

set -Eeo pipefail
trap "pipeline_notification 'fail' && exit 1" ERR

echo "[INFO] Installing serverless framework and required plugins"
npm install -g serverless
cd backend
npm install
cd ..

# Deploy the backend using serverless framework
make deploy-backend

echo "[INFO] Installing terraform"
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://rpm.releases.hashicorp.com/AmazonLinux/hashicorp.repo
sudo yum -y install terraform

# Deploy the terraform
cd terraform
make init
make apply
cd ..
