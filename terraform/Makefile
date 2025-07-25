ENV_VAR_FILE := "./environments/${BUILD_ENV}/terraform.tfvars"
BACKEND_CONF := "./environments/${BUILD_ENV}/backend.conf"

init:
	@echo "[INFO] Removing cached terraform modules"
	@rm -rf .terraform/modules
	@echo "[INFO] Initialiasing terraform in ${BUILD_ENV} environment"
	@terraform init -reconfigure -backend-config=${BACKEND_CONF}
	@echo "[INFO] Validating terraform code"
	@terraform validate

validate:
	@echo "[INFO] Validating terraform code"
	@terraform validate

plan:
	@echo "[INFO] Running a terraform plan in ${BUILD_ENV} environment"
	@terraform plan -parallelism=30 -refresh=true -out=plan.out -var-file=${ENV_VAR_FILE}

apply:
	@echo "[INFO] Deploying the infrastructure in ${BUILD_ENV} environment"
	@terraform apply -auto-approve -var-file=${ENV_VAR_FILE}

destroy:
	@echo "[INFO] Destroying the deployment in ${BUILD_ENV} environment"
	@terraform destroy -auto-approve -var-file=${ENV_VAR_FILE}
	@echo "Deployment is completed on Services Forecasting API in ${BUILD_ENV} environment"
