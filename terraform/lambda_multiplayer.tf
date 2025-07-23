resource "aws_iam_role" "multiplayer_execution_role" {
  name = "${var.app-name}_multiplayer_execution_role_${var.environment}"

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

resource "aws_iam_policy" "multiplayer_execution_policy" {
  name = "${var.app-name}_multiplayer-lambda-execution-policy_${var.environment}"

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
          "dynamodb:GetItem",
          "dynamodb:Query",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem"
        ]
        Resource = aws_dynamodb_table.player-table.arn
      },
      {
        Effect   = "Allow"
        Action   = ["dynamodb:Query"]
        Resource = "${aws_dynamodb_table.player-table.arn}/index/LobbyIndex"
      },
      {
        Effect = "Allow"
        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem"
        ]
        Resource = aws_dynamodb_table.lobby-table.arn
      },
      {
        Effect   = "Allow"
        Action   = ["execute-api:ManageConnections"]
        Resource = "${aws_apigatewayv2_api.multiplayer_api.execution_arn}/${aws_apigatewayv2_stage.multiplayer_stage.name}/POST/@connections/*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "multiplayer_execution_policy_attachment" {
  role       = aws_iam_role.multiplayer_execution_role.name
  policy_arn = aws_iam_policy.multiplayer_execution_policy.arn
}

resource "aws_lambda_function" "multiplayer_server" {
  function_name    = "${var.app-name}-multiplayer-server-${var.environment}"
  runtime          = "python3.13"
  role             = aws_iam_role.multiplayer_execution_role.arn
  handler          = "multiplayer_server.lambda_handler"
  timeout          = 25
  memory_size      = 512
  filename         = "${path.module}/../backend/build/multiplayer_server.zip"
  source_code_hash = filebase64sha256("${path.module}/../backend/build/multiplayer_server.zip")

  environment {
    variables = {
      MULTIPLAYER_ENDPOINT = "${aws_apigatewayv2_api.multiplayer_api.api_endpoint}/${aws_apigatewayv2_stage.multiplayer_stage.name}"
      PLAYER_TABLE_NAME    = aws_dynamodb_table.player-table.name
      LOBBY_TABLE_NAME     = aws_dynamodb_table.lobby-table.name
    }
  }
}
