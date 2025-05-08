resource "aws_iam_role" "update_airports_execution_role" {
  name = "${var.app-name}_update_airports_execution_role_${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_policy" "update_airports_execution_policy" {
  name = "${var.app-name}_update_airports-lambda-execution-policy_${var.environment}"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      },
      {
        Effect   = "Allow"
        Action   = ["s3:PutObject"]
        Resource = "${aws_s3_bucket.host-bucket.arn}/airports.json"
      },
    ]
  })
}

resource "aws_iam_role_policy_attachment" "update_airports_execution_policy_attachment" {
  role       = aws_iam_role.update_airports_execution_role.name
  policy_arn = aws_iam_policy.update_airports_execution_policy.arn
}

resource "aws_lambda_function" "update_airports" {
  function_name    = "${var.app-name}-update_airports-${var.environment}"
  runtime          = "python3.13"
  role             = aws_iam_role.update_airports_execution_role.arn
  handler          = "update_airports.lambda_handler"
  timeout          = 30
  memory_size      = 512
  filename         = "${path.module}/../backend/build/update_airports.zip"
  source_code_hash = filebase64sha256("${path.module}/../backend/build/update_airports.zip")

  environment {
    variables = {
      BUCKET_NAME = aws_s3_bucket.host-bucket.id
    }
  }
}
