resource "aws_cloudfront_distribution" "cdn" {
  enabled         = true
  is_ipv6_enabled = true
  price_class     = "PriceClass_100"
  aliases         = [var.full_domain]

  origin {
    domain_name = aws_s3_bucket_website_configuration.host-bucket-hosting-config.website_endpoint
    origin_id   = "${var.service}-cloudfront"
    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "https-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }

  default_cache_behavior {
    target_origin_id       = "${var.service}-cloudfront"
    allowed_methods        = ["GET", "HEAD"]
    cached_methods         = ["GET", "HEAD"]
    compress               = false
    viewer_protocol_policy = "redirect-to-https"
    cache_policy_id        = aws_cloudfront_cache_policy.cf_cache_policy.id
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    acm_certificate_arn = "arn:aws:acm:us-east-1:082862148481:certificate/2ba2a539-daeb-4076-9e7a-bc2a6526e157"
    ssl_support_method  = "sni-only"
  }

  tags = {
    Name = "${var.service}-cloudfront"
  }
}

resource "aws_cloudfront_cache_policy" "cf_cache_policy" {
  name        = "${var.service}-${var.environment}-cf"
  comment     = "Cache policy for the ${var.service} application"
  default_ttl = 86400
  max_ttl     = 604800
  min_ttl     = 21600

  parameters_in_cache_key_and_forwarded_to_origin {
    enable_accept_encoding_brotli = true
    enable_accept_encoding_gzip   = true
    cookies_config {
      cookie_behavior = "none"
    }
    headers_config {
      header_behavior = "none"
    }
    query_strings_config {
      query_string_behavior = "none"
    }
  }
}
