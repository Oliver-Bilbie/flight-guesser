resource "aws_apigatewayv2_api" "multiplayer_api" {
  name                       = "${var.app-name} multiplayer (${var.environment})"
  protocol_type              = "WEBSOCKET"
  route_selection_expression = "$request.body.action"
}

resource "aws_apigatewayv2_stage" "multiplayer_stage" {
  api_id      = aws_apigatewayv2_api.multiplayer_api.id
  name        = var.environment
  auto_deploy = true
}

resource "aws_apigatewayv2_route" "connect_route" {
  api_id    = aws_apigatewayv2_api.multiplayer_api.id
  route_key = "$connect"

  target = "integrations/${aws_apigatewayv2_integration.connect_integration.id}"
}

resource "aws_apigatewayv2_route" "disconnect_route" {
  api_id    = aws_apigatewayv2_api.multiplayer_api.id
  route_key = "$disconnect"

  target = "integrations/${aws_apigatewayv2_integration.disconnect_integration.id}"
}

resource "aws_apigatewayv2_route" "handle_guess_route" {
  api_id    = aws_apigatewayv2_api.multiplayer_api.id
  route_key = "handle_guess"

  target = "integrations/${aws_apigatewayv2_integration.handle_guess_integration.id}"
}

resource "aws_apigatewayv2_integration" "connect_integration" {
  api_id             = aws_apigatewayv2_api.multiplayer_api.id
  integration_type   = "AWS_PROXY"
  integration_uri    = aws_lambda_function.multiplayer_server.arn
  integration_method = "POST"
}

resource "aws_apigatewayv2_integration" "disconnect_integration" {
  api_id             = aws_apigatewayv2_api.multiplayer_api.id
  integration_type   = "AWS_PROXY"
  integration_uri    = aws_lambda_function.multiplayer_server.arn
  integration_method = "POST"
}

resource "aws_apigatewayv2_integration" "handle_guess_integration" {
  api_id             = aws_apigatewayv2_api.multiplayer_api.id
  integration_type   = "AWS_PROXY"
  integration_uri    = aws_lambda_function.multiplayer_server.arn
  integration_method = "POST"
}

resource "aws_lambda_permission" "connect_permission" {
  statement_id  = "AllowAPIGatewayConnect"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.multiplayer_server.arn
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.multiplayer_api.execution_arn}/*"
}

resource "aws_lambda_permission" "disconnect_permission" {
  statement_id  = "AllowAPIGatewayDisconnect"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.multiplayer_server.arn
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.multiplayer_api.execution_arn}/*"
}

resource "aws_lambda_permission" "handle_guess_permission" {
  statement_id  = "AllowAPIGatewayResetTime"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.multiplayer_server.arn
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.multiplayer_api.execution_arn}/*"
}

output "multiplayer_endpoint" {
  value = "${aws_apigatewayv2_api.multiplayer_api.api_endpoint}/${aws_apigatewayv2_stage.multiplayer_stage.name}"
}
