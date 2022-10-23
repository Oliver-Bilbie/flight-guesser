BUILD_ENV = "development"
ENV_VAR_FILE := "./environments/${BUILD_ENV}.tfvars"

init:
	@echo "[INFO] Removing cached terraform modules"
	@rm -Rf .terraform/modules
	@echo "[INFO] Initialiasing terraform in ${BUILD_ENV} environment"
	@terraform init -reconfigure
	@echo "[INFO] Validating terraform code"
	@terraform validate

validate:
	@echo "[INFO] Validating terraform code"
	@terraform validate

plan:
	@echo "[INFO] Running a terraform plan in ${BUILD_ENV} environment"
	@terraform plan -parallelism=30 -refresh=true -out=plan.out -var-file=${ENV_VAR_FILE}

apply: validate
	@echo "[INFO] Deploying the infrastructure in ${BUILD_ENV} environment"
	@terraform apply -auto-approve -var-file=${ENV_VAR_FILE}

destroy:
	@echo "[INFO] Destroying the deployment in ${BUILD_ENV} environment"
	@terraform destroy -auto-approve -var-file=${ENV_VAR_FILE}
	@echo "Deployment is completed on Services Forecasting API in ${BUILD_ENV} environment"
