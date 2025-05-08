resource "aws_cloudwatch_event_rule" "update_airports" {
  name                = "${var.app-name}-update-airports"
  schedule_expression = "cron(0 0 * * ? *)"
}

resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.update_airports.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.update_airports.arn
}

resource "aws_cloudwatch_event_target" "invoke_lambda" {
  rule      = aws_cloudwatch_event_rule.update_airports.name
  target_id = "UpdateAirportsLambda"
  arn       = aws_lambda_function.update_airports.arn
}
