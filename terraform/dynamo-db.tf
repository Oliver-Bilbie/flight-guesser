resource "aws_dynamodb_table" "player-table" {
  name           = "flight-guesser-player-table-${var.environment}"
  billing_mode   = "PROVISIONED"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "player_id"
  range_key      = "lobby_id"

  attribute {
    name = "player_id"
    type = "S"
  }

  attribute {
    name = "player_name"
    type = "S"
  }

  attribute {
    name = "lobby_id"
    type = "S"
  }

  global_secondary_index {
    name               = "LobbyIndex"
    hash_key           = "lobby_id"
    range_key          = "player_name"
    write_capacity     = 5
    read_capacity      = 5
    projection_type    = "ALL"
  }

  tags = {
    Name        = "flight-guesser-player-table-${var.environment}"
    Description = "DynamoDB table to store player data for the flight-guesser application"
    Environment = "${var.environment}"
  }
}


resource "aws_dynamodb_table" "lobby-table" {
  name           = "flight-guesser-lobby-table-${var.environment}"
  billing_mode   = "PROVISIONED"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "lobby_id"

  attribute {
    name = "lobby_id"
    type = "S"
  }

  tags = {
    Name        = "flight-guesser-lobby-table-${var.environment}"
    Description = "DynamoDB table to store lobby data for the flight-guesser application"
    Environment = "${var.environment}"
  }
}
