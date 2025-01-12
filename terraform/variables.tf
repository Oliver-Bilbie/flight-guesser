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

variable "base_domain" {
  type        = string
  description = "Name of the Route53 hosted zone domain"
}

variable "full_domain" {
  type        = string
  description = "Name of the domain to host the webapp"
}

variable "cert_arn" {
  type        = string
  description = "ARN of the ACM certificate for full_domain"
}
