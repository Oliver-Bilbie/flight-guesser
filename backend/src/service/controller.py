"""Controllers for AWS Lambda functions"""

import json
from src.service import service


def get_airports():
    """
    Controller for the get_airports Lambda function, which returns a
    complete list of airport names.

    Returns a json object with:
        "response": a list of airport names
        "status": request status code
    """

    try:
        airport_names = service.get_airports()
        response = json.dumps({"response": airport_names, "status": 200})

    except:
        response = json.dumps({"response": "An error has occurred.", "status": 500})

    return response


def handle_turn(longitude, latitude, origin, destination, player_id):
    """
    Controller for the handle_turn Lambda function, which returns data
    corresponding to the closest flight to a provided longitude-latitude
    pair along with a score based on the proximity of a destination guess.
    If a player_id is provided, the dynamo table will be updated to reflect
    any points scored.

    Args:
        longitude [float]: longitude to search from
        latitude [float]: latitude to search from
        origin [string]: origin airport guess
        destination [string]: destination airport guess
        player_id [string]: ID of the player

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

    try:
        flight = service.get_closest_flight(longitude, latitude)

        if flight is None:
            response = json.dumps({"response": "No flights were found", "status": 400})
        else:
            score = service.get_score(flight, origin, destination)

            if player_id != "":
                service.update_player_score(player_id, score)

            response = json.dumps(
                {
                    "response": {
                        "id": flight.id,
                        "origin": flight.origin_airport_name,
                        "destination": flight.destination_airport_name,
                        "aircraft": flight.aircraft_code,
                        "score": score,
                    },
                    "status": 200,
                }
            )

    except:
        response = json.dumps({"response": "An error has occurred.", "status": 500})

    return response


def create_lobby(name, score, guessed_flights, rules):
    """
    Controller for the create_lobby Lambda function, which generates a unique
    four-letter code to identify a lobby and then creates an entry in the
    dynamo table corresponding to the player.

    Args:
        name [string]: Name of the player
        score [string]: Score of the player
        guessed_flights [string[]]: Flight IDs previously guessed by the player
        rules [integer]: Integer encoded ruleset of the lobby

    Returns a json object with:
        "response": a json object with:
            "player_id": unique ID for the player
            "lobby_id": unique ID of the lobby
        "status": request status code
    """

    try:
        lobby_id = service.get_unique_lobby_id()
        player_id = service.create_player_data(
            lobby_id, name, score, guessed_flights, rules
        )
        lobby_data = str(
            [
                {
                    "name": name,
                    "player_id": player_id,
                    "score": score,
                }
            ]
        )
        response = json.dumps(
            {
                "response": {
                    "lobby_id": lobby_id,
                    "player_id": player_id,
                    "lobby_data": lobby_data,
                },
                "status": 200,
            }
        )

    except:
        response = json.dumps({"response": "An error has occurred.", "status": 500})

    return response


def join_lobby(lobby_id, name, score, guessed_flights):
    """
    Controller for the join_lobby Lambda function, which creates an entry in
    the dynamo table corresponding to the player. Returns a list of
    current players in the lobby and their corresponding scores.

    Args:
        lobby_id [string]: ID of the lobby to join
        name [string]: Name of the player
        score [string]: Score of the player
        guessed_flights [string[]]: Flight IDs previously guessed by the player

    Returns a json object with:
        "response": a json object with:
            "player_id": unique ID for the player
            "guessed_flights": a list of previous guessed flight IDs
            "rules": enum of the ruleset of the lobby
            "lobby_data": [{"name": string, "score": string}, ...]
        "status": request status code
    """

    try:
        # Check that lobby exists and get the corresponding rules

        # Check whether the player already exists in the lobby
        player_id = service.get_player_id(lobby_id, name)
        if player_id == "":  # If the player does not have an ID, create a new one
            player_id = service.create_player_data(
                lobby_id, name, score, guessed_flights, rules
            )

        # Get the latests scores for players in the lobby
        lobby_data = service.get_lobby_scores(lobby_id)

        response = json.dumps(
            {
                "response": {"player_id": player_id, "lobby_data": lobby_data},
                "status": 200,
            }
        )

    except:
        response = json.dumps({"response": "An error has occurred.", "status": 500})

    return response


def get_lobby_scores(lobby_id):
    """
    Controller for the get_lobby_scores Lambda function, which returns a list of
    current players in the lobby and their corresponding scores.

    Args:
        lobby_id [string]: ID of the lobby

    Returns a json object with:
        "response": [{"name": string, "score": string}, ...]
        "status": request status code
    """

    try:
        lobby_data = service.get_lobby_scores(lobby_id)

        response = json.dumps({"response": lobby_data, "status": 200})

    except:
        response = json.dumps({"response": "An error has occurred.", "status": 500})

    return response
