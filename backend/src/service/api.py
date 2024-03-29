"""
Handlers for AWS Lambda functions

Some of these functions are sinkholes which are here to fit the project pattern
of API, controller, and service layers. This pattern is not ideal now that the
project has grown and may be refactored in the future.
"""

import json
from src.service import service, controller


def get_airports(_event, _context):
    """
    Handler for the get_airports Lambda function, which returns a
    complete list of airport names.

    Args:
        event: AWS Lambda event
        context: AWS Lambda context

    Returns a json object with:
        "response": a list of airport names
        "status": request status code
    """

    response = controller.get_airports()

    return response


def handle_turn(event, _context):
    """
    Handler for the handle_turn Lambda function, which returns data
    corresponding to the closest flight to a provided longitude-latitude
    pair along with a score based on the proximity of an origin and
    destination guess.

    Args:
        event: AWS Lambda event. "body" should be a json string containing
            "longitude", "latitude", "origin", "destination", and "player_id".
        context: AWS Lambda context

    Returns a json object with:
        "response":
            on success, a json object with:
                "id": id of the nearest aircraft
                "origin": origin of the nearest aircraft
                "destination": destination of the nearest aircraft
                "aircraft": model of the nearest aircraft
                "score": points earned by the player
            on failure:
                string: error message
        "status": request status code
    """

    body = event.get("body")
    body = json.loads(body)
    longitude = body.get("longitude")
    latitude = body.get("latitude")
    origin = body.get("origin")
    destination = body.get("destination")
    player_id = body.get("player_id")

    response = controller.handle_turn(
        longitude, latitude, origin, destination, player_id
    )

    return response


def create_lobby(event, _context):
    """
    Handler for the create_lobby Lambda function, which generates a unique
    four-letter code to identify a lobby and then creates an entry in the
    dynamo table corresponding to the player.

    Args:
        event: AWS Lambda event. "body" should be a json string containing
            "name", "score", "guessed_flights", and "rules".
        context: AWS Lambda context

    Returns a json object with:
        "response": a json object with:
            "player_id": unique ID for the player
            "lobby_id": unique ID of the lobby
        "status": request status code
    """

    body = event.get("body")
    body = json.loads(body)
    name = body.get("name")
    score = body.get("score")
    guessed_flights = body.get("guessed_flights")
    rules = body.get("rules")

    response = controller.create_lobby(name, score, guessed_flights, rules)

    return response


def join_lobby(event, _context):
    """
    Handler for the join_lobby Lambda function, which creates an entry in
    the dynamo table corresponding to the player. Returns a list of
    current players in the lobby and their corresponding scores.

    Args:
        event: AWS Lambda event. "body" should be a json string containing
            "lobby_id", "name", "score", and "guessed_flights".
        context: AWS Lambda context

    Returns a json object with:
        "response": a json object with:
            "player_id": unique ID for the player
            "guessed_flights": a list of previous guessed flight IDs
            "rules": enum of the ruleset of the lobby
            "lobby_data": [{"name": string, "score": string}, ...]
        "status": request status code
    """

    body = event.get("body")
    body = json.loads(body)
    lobby_id = body.get("lobby_id")
    name = body.get("name")
    score = body.get("score")
    guessed_flights = body.get("guessed_flights")

    response = controller.join_lobby(lobby_id, name, score, guessed_flights)

    return response


def get_lobby_scores(event, _context):
    """
    Handler for the get_lobby_scores Lambda function, which returns a list of
    current players in the lobby and their corresponding scores.

    Args:
        event: AWS Lambda event. "body" should be a json string containing
            "lobby_id"
        context: AWS Lambda context

    Returns a json object with:
        "response":
            on success:
                [{"name": string, "score": string}, ...]
            on failure:
                string: error message
        "status": request status code
    """

    lobby_id = event.get("pathParameters").get("lobby_id")
    response = controller.get_lobby_scores(lobby_id)

    return response


def delete_lobby(_event, _context):
    """
    Handler for the delete_lobby Lambda function, which runs from a cron event
    to delete old lobby data from dynamo.

    Args:
        event: AWS Lambda event
        context: AWS Lambda context
    """

    service.delete_old_data()
