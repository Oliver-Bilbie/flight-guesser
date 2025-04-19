resource "aws_iam_role" "singleplayer_execution_role" {
  name = "${var.app-name}_singleplayer_execution_role"

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
  name = "singleplayer-lambda-execution-policy"

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
        Effect = "Allow"
        Action = [
          "dynamodb:Query",
          "dynamodb:Scan",
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem"
        ]
        Resource = aws_dynamodb_table.player-table.arn
      },
      {
        Effect = "Allow"
        Action = [
          "dynamodb:Query",
          "dynamodb:Scan",
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem"
        ]
        Resource = aws_dynamodb_table.lobby-table.arn
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "singleplayer_execution_policy_attachment" {
  role       = aws_iam_role.singleplayer_execution_role.name
  policy_arn = aws_iam_policy.singleplayer_execution_policy.arn
}

resource "aws_lambda_function" "singleplayer" {
  function_name    = "${var.app-name}-singleplayer"
  runtime          = "python3.13"
  role             = aws_iam_role.singleplayer_execution_role.arn
  handler          = "singleplayer_server.lambda_handler"
  timeout          = 10
  memory_size      = 256
  filename         = "${path.module}/../backend/build/server.zip"
  source_code_hash = filebase64sha256("${path.module}/../backend/build/server.zip")

  environment {
    variables = {
      PLAYER_TABLE_NAME = aws_dynamodb_table.player-table.name
      LOBBY_TABLE_NAME  = aws_dynamodb_table.lobby-table.name
    }
  }
}
