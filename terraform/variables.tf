variable "region" {
  type        = string
  description = "Name of the AWS region all AWS resources will be provisioned in"
}

variable "service" {
  type        = string
  description = "Name of the service"
}

variable "environment" {
  type        = string
  description = "Name of the deployment environment"
}

variable "deployment_bucket" {
  type        = string
  description = "Name of the S3 bucket where the frontend code will be deployed"
}
