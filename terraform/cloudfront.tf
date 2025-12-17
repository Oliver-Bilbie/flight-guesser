data "aws_cloudfront_origin_request_policy" "cors_request_policy" {
  name = "Managed-CORS-S3Origin"
}

data "aws_cloudfront_response_headers_policy" "cors_response_policy" {
  name = "Managed-CORS-with-preflight-and-SecurityHeadersPolicy"
}

resource "aws_cloudfront_distribution" "cdn" {
  enabled         = true
  is_ipv6_enabled = true
  price_class     = "PriceClass_100"
  aliases         = [var.full_domain]

  origin {
    domain_name = aws_s3_bucket_website_configuration.host-bucket-hosting-config.website_endpoint
    origin_id   = "${var.app-name}-cloudfront"
    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "http-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }

  ordered_cache_behavior {
    path_pattern               = "/airports.json"
    target_origin_id           = "${var.app-name}-cloudfront"
    allowed_methods            = ["GET", "HEAD"]
    cached_methods             = ["GET", "HEAD"]
    compress                   = true
    viewer_protocol_policy     = "redirect-to-https"
    cache_policy_id            = aws_cloudfront_cache_policy.airports_cache.id
    origin_request_policy_id   = data.aws_cloudfront_origin_request_policy.cors_request_policy.id
    response_headers_policy_id = data.aws_cloudfront_response_headers_policy.cors_response_policy.id
  }

  default_cache_behavior {
    target_origin_id           = "${var.app-name}-cloudfront"
    allowed_methods            = ["GET", "HEAD"]
    cached_methods             = ["GET", "HEAD"]
    compress                   = true
    viewer_protocol_policy     = "redirect-to-https"
    cache_policy_id            = aws_cloudfront_cache_policy.static_cache.id
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    acm_certificate_arn = var.cert_arn
    ssl_support_method  = "sni-only"
  }

  tags = {
    Name = "${var.app-name}-cloudfront"
  }
}

resource "aws_cloudfront_cache_policy" "airports_cache" {
  name        = "${var.app-name}-${var.environment}-airports-cache"
  comment     = "Cache policy for airport data for the ${var.app-name} application"
  default_ttl = 43200
  max_ttl     = 86400
  min_ttl     = 0

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

resource "aws_cloudfront_cache_policy" "static_cache" {
  name        = "${var.app-name}-${var.environment}-static-cache"
  comment     = "Cache policy for static files for the ${var.app-name} application"
  default_ttl = 86400
  max_ttl     = 604800
  min_ttl     = 86400

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

output "cloudfront_distribution" {
  value = aws_cloudfront_distribution.cdn.id
}

output "airports_endpoint" {
  value = "https://${var.full_domain}/airports.json"
}
