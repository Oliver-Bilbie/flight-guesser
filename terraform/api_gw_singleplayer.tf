resource "aws_apigatewayv2_api" "singleplayer_api" {
  name                       = "${var.app-name} singleplayer (${var.environment})"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_stage" "singleplayer_stage" {
  api_id      = aws_apigatewayv2_api.singleplayer_api.id
  name        = var.environment
  auto_deploy = true
}

resource "aws_apigatewayv2_route" "make_guess_route" {
  api_id    = aws_apigatewayv2_api.singleplayer_api.id
  route_key = "POST /guess"

  target = "integrations/${aws_apigatewayv2_integration.make_guess_integration.id}"
}

resource "aws_apigatewayv2_integration" "make_guess_integration" {
  api_id             = aws_apigatewayv2_api.singleplayer_api.id
  integration_type   = "AWS_PROXY"
  integration_uri    = aws_lambda_function.singleplayer.arn
  integration_method = "POST"
}

resource "aws_lambda_permission" "make_guess_permission" {
  statement_id  = "AllowAPIGatewayConnect"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.singleplayer.arn
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.singleplayer_api.execution_arn}/*"
}

output "singleplayer_endpoint" {
  value = "${aws_apigatewayv2_api.singleplayer_api.api_endpoint}/${aws_apigatewayv2_stage.singleplayer_stage.name}"
}
