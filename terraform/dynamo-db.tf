resource "aws_dynamodb_table" "lobby-table" {
  name           = "flight-guesser-lobby-table-${var.environment}"
  billing_mode   = "PROVISIONED"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "player_id"

  attribute {
    name = "player_id"
    type = "S"
  }

  tags = {
    Name        = "flight-guesser-lobby-table-${var.environment}"
    Description = "DynamoDB table to facilitate multiplayer lobby functionality in the flight-guesser app"
    Environment = "${var.environment}"
  }
}