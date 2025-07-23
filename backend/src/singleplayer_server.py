"""
HTTP API for handling singleplayer requests
"""

import traceback
import json
from dataclasses import asdict
from helpers.make_guess import make_guess
from helpers.utils import HandledException, read_position, read_rules


def lambda_handler(event, context):
    try:
        input_body = json.loads(event.get("body"))
        rules = read_rules(input_body.get("rules"))
        player_position = read_position(
            input_body.get("player"),
            "player",
            allow_missing=False,
        )
        origin_guess_pos = read_position(
            input_body.get("origin"),
            "origin airport",
            allow_missing=(not rules.use_origin),
        )
        destination_guess_pos = read_position(
            input_body.get("destination"),
            "destination airport",
            allow_missing=(not rules.use_destination),
        )

        guess_result = make_guess(
            player_position,
            origin_guess_pos,
            destination_guess_pos,
            rules,
        )

        return {
            "statusCode": 200,
            "body": json.dumps(asdict(guess_result)),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": False,
            },
            "isBase64Encoded": False,
        }

    except HandledException as exc:
        return exc.to_http_response()

    except Exception as exc:
        print(f"[ERROR] {str(exc)}")
        print(traceback.format_exc())
        return {
            "statusCode": 500,
            "body": json.dumps(
                {"message": "The server was unable to process your request"}
            ),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": False,
            },
            "isBase64Encoded": False,
        }
