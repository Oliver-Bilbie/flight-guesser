!/bin/bash

set -Eeo pipefail
trap "pipeline_notification 'fail' && exit 1" ERR

echo "[INFO] Installing serverless framework and required plugins"
npm install -g serverless
cd backend && npm install

echo "[INFO] Installing terraform"
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://rpm.releases.hashicorp.com/AmazonLinux/hashicorp.repo
sudo yum -y install terraform

make deploy-backend
cd terraform && make init
cd terraform && make apply
