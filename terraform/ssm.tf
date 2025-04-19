resource "aws_ssm_parameter" "host-bucket" {
  name        = "${var.app-name}-${var.environment}-host-bucket"
  description = "The bucket where the static website for ${var.app-name} is hosted"
  type        = "String"
  value       = aws_s3_bucket.host-bucket.bucket
}

resource "aws_ssm_parameter" "cdn-id" {
  name        = "${var.app-name}-${var.environment}-cdn-id"
  description = "The CloudFront distribution ID for ${var.app-name}"
  type        = "String"
  value       = aws_cloudfront_distribution.cdn.id
}
