resource "aws_s3_bucket" "host-bucket" {
  bucket = var.deployment_bucket
}

resource "aws_s3_bucket_public_access_block" "host-bucket-public-access" {
  bucket                  = aws_s3_bucket.host-bucket.id
  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_policy" "allow_access" {
  bucket = aws_s3_bucket.host-bucket.id
  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Sid" : "PublicReadGetObject",
        "Effect" : "Allow",
        "Principal" : "*",
        "Action" : "s3:GetObject",
        "Resource" : "${aws_s3_bucket.host-bucket.arn}/*"
      }
    ]
  })
}

resource "aws_s3_bucket_cors_configuration" "host-bucket-cors" {
  bucket = aws_s3_bucket.host-bucket.id

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET"]
    allowed_origins = ["*"]
  }
}

resource "aws_s3_bucket_website_configuration" "host-bucket-hosting-config" {
  bucket = aws_s3_bucket.host-bucket.id
  index_document {
    suffix = "index.html"
  }
}
