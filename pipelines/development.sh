!/bin/bash

echo "[INFO] Installing serverless framework"
npm install -g serverless

echo "[INFO] Installing terraform"
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://rpm.releases.hashicorp.com/AmazonLinux/hashicorp.repo
sudo yum -y install terraform

make deploy-backend
cd terraform && make init
cd terraform && make apply
