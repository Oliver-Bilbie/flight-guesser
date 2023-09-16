bootstrap: install-dev-deps
	@pre-commit install

install-pipeline-deps: install-python-deps install-node-deps install-serverless install-terraform

install-python-deps:
	@cd backend && python -m pipenv install

install-node-deps:
	@cd frontend && yarn --production

install-serverless:
	@yarn

install-terraform:
	@yum install -y yum-utils
	@yum-config-manager --add-repo https://rpm.releases.hashicorp.com/AmazonLinux/hashicorp.repo
	@yum -y install terraform

install-dev-deps: install-python-dev-deps install-node-dev-deps

install-python-dev-deps:
	@cd backend && python -m pipenv install --dev

install-node-dev-deps:
	@cd frontend && yarn

format-src:
	@echo "[INFO] Formatting backend source code using black"
	@cd backend && python -m pipenv run black src
	@echo "[INFO] Formatting frontend source code using prettier"
	@cd frontend && yarn pretty

test-all: lint unit-test int-test frontend-test

lint:
	@echo "[INFO] Linting backend source code using pylint"
	@cd backend && python -m pipenv run pylint --fail-under 7.5 src/service/*
	@echo "[INFO] Linting source code using bandit to look for common security issues in python source"
	@cd backend && python -m pipenv run bandit -r src/serivce
	@echo "[INFO] Linting frontend source code using eslint"
	@cd frontend && yarn lint

unit-test:
	@echo "[INFO] Running unit tests"
	@cd backend && export COVERAGE_FILE=./target/coverage/.cov_unit && python -m pipenv run coverage run --source=src/service -m pytest -s --junitxml=target/unit-test/unit-result.xml src/test/unit/*.py
	@cd backend && export COVERAGE_FILE=./target/coverage/.cov_unit && python -m pipenv run coverage html --directory=target/unit-test/coverage --fail-under=80
	@cd backend && export COVERAGE_FILE=./target/coverage/.cov_unit && python -m pipenv run coverage report
	@cd backend && export COVERAGE_FILE=./target/coverage/.cov_unit && python -m pipenv run coverage xml -o target/unit-test/coverage/coverage.xml

int-test:
	@echo "[INFO] Running component integration tests"
	@cd backend && export COVERAGE_FILE=./target/coverage/.cov_int && python -m pipenv run coverage run --source=src/service -m pytest -s --junitxml=target/integration-test/integration-result.xml src/test/integration/*.py
	@cd backend && export COVERAGE_FILE=./target/coverage/.cov_int && python -m pipenv run coverage html --directory=target/integration-test/coverage --fail-under=50
	@cd backend && export COVERAGE_FILE=./target/coverage/.cov_int && python -m pipenv run coverage report
	@cd backend && export COVERAGE_FILE=./target/coverage/.cov_int && python -m pipenv run coverage xml -o target/integration-test/coverage/coverage.xml

frontend-test:
	@echo "[INFO] Running frontend tests"
	@cd frontend && yarn test

deploy-terraform:
	@echo "[INFO] Deploying infrastructure to ${STAGE} environment"
	@cd terraform && terraform init -reconfigure -backend-config="./environments/${STAGE}/backend.conf"
	@cd terraform && terraform validate
	@cd terraform && terraform apply -auto-approve -var-file="./environments/${STAGE}/terraform.tfvars"

deploy-backend:
	@echo "[INFO] Deploying backend to ${STAGE} environment"
	@cd backend && pipenv requirements > requirements.txt
	@cd backend && npx sls deploy -s ${STAGE}

deploy-frontend:
	@echo "[INFO] Deploying frontend to ${STAGE} environment"
	@cd frontend && yarn build:${STAGE}
	@cd frontend && aws s3 cp build "s3://${DEPLOY_BUCKET_NAME}" --recursive
	@aws cloudfront create-invalidation --distribution-id ${CF_DISTRIBUTION_ID} --paths "/*"
