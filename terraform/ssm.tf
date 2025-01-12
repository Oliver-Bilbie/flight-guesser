resource "aws_ssm_parameter" "host-bucket" {
  name        = "${var.service}-${var.environment}-host-bucket"
  description = "The bucket where the static website for ${var.service} is hosted"
  type        = "String"
  value       = aws_s3_bucket.host-bucket.bucket
}

resource "aws_ssm_parameter" "cdn-id" {
  name        = "${var.service}-${var.environment}-cdn-id"
  description = "The CloudFront distribution ID for ${var.service}"
  type        = "String"
  value       = aws_cloudfront_distribution.cdn.id
}
