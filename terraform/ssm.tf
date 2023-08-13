resource "aws_ssm_parameter" "host-bucket" {
  name        = "${var.service}-${var.environment}-host-bucket"
  description = "The bucket where the static website for ${var.service} is hosted"
  type        = "String"
  value       = aws_s3_bucket.host-bucket.bucket
}
