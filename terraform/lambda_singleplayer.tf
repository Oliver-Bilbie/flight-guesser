resource "aws_iam_role" "singleplayer_execution_role" {
  name = "${var.app-name}_singleplayer_execution_role_${var.environment}"

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

resource "aws_iam_policy" "singleplayer_execution_policy" {
  name = "${var.app-name}_singleplayer-lambda-execution-policy_${var.environment}"

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
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "singleplayer_execution_policy_attachment" {
  role       = aws_iam_role.singleplayer_execution_role.name
  policy_arn = aws_iam_policy.singleplayer_execution_policy.arn
}

resource "aws_lambda_function" "singleplayer" {
  function_name    = "${var.app-name}-singleplayer-server-${var.environment}"
  runtime          = "python3.13"
  role             = aws_iam_role.singleplayer_execution_role.arn
  handler          = "singleplayer_server.lambda_handler"
  timeout          = 10
  memory_size      = 256
  filename         = "${path.module}/../backend/build/singleplayer_server.zip"
  source_code_hash = filebase64sha256("${path.module}/../backend/build/singleplayer_server.zip")
}
