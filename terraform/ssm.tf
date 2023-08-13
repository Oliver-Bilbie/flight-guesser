resource "aws_ssm_parameter" "host-bucket" {
  name = "${aws_s3_bucket.host-bucket.bucket}-ssm"
  description = "The bucket where the static website for ${var.service} is hosted"
  type = "String"
  value = "${aws_s3_bucket.host-bucket.bucket}"
}
