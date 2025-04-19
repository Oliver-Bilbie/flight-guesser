import json
from dataclasses import asdict
from data_types import Position, AirportGuess
from make_guess import make_guess


def lambda_handler(event, context):
    try:
        print(f"Received event: {event}")
        input_body = json.loads(event.get("body"))

        print(f"Body: {input_body}")
        player_position = Position(
            lon=input_body.get("player").get("lon"),
            lat=input_body.get("player").get("lat"),
        )
        origin = AirportGuess(
            position=Position(
                lon=input_body.get("origin").get("lon"),
                lat=input_body.get("origin").get("lat"),
            ),
            enabled=input_body.get("origin").get("enabled"),
        )
        destination = AirportGuess(
            position=Position(
                lon=input_body.get("destination").get("lon"),
                lat=input_body.get("destination").get("lat"),
            ),
            enabled=input_body.get("destination").get("enabled"),
        )

        guess_result = make_guess(player_position, origin, destination)

        if guess_result.success:
            return {
                "statusCode": 200,
                "body": json.dumps(asdict(guess_result)),
            }

        return {
            "statusCode": 404,
            "body": json.dumps(asdict(guess_result)),
        }

    except Exception as exc:
        return {"statusCode": 500, "body": json.dumps({"error": str(exc)})}
