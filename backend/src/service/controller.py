"""Controllers for AWS Lambda functions"""

import json
from src.service import service, validator


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
        response = json.dumps({"response": "An error has occurred", "status": 500})

    return response


def handle_turn(longitude, latitude, origin, destination, player_id):
    """
    Controller for the handle_turn Lambda function, which returns data
    corresponding to the closest flight to a provided longitude-latitude
    pair along with a score based on the proximity of a destination guess.
    If a player_id is provided, the dynamo table will be updated to reflect
    any points scored.
    Args:
        longitude [string]: longitude to search from
        latitude [string]: latitude to search from
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
        # Validate user inputs
        if not validator.validate_position(longitude, latitude):
            response = json.dumps({"response": "Invalid position", "status": 400})
        elif not validator.validate_airport_names(origin, destination):
            response = json.dumps({"response": "Invalid airport names", "status": 400})
        elif not validator.validate_player_id(player_id):
            response = json.dumps({"response": "Invalid player ID", "status": 400})

        else:  # If validation is successful
            flight = service.get_closest_flight(float(longitude), float(latitude))

            if flight is None:
                response = json.dumps(
                    {"response": "No flights were found", "status": 400}
                )
            else:
                # Check that the guess conforms to the rules
                ### come back to this
                print(f"Lobby Rules: {service.get_lobby_rules()}")

                # Confirm that a guess has not already been made for this flight
                ### come back to this
                print(f"Previous Guesses: {service.get_player_guesses()}")

                score = service.get_score(flight, origin, destination)

                if player_id != "":
                    service.update_player_data(player_id, score, flight.id)

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
        response = json.dumps({"response": "An error has occurred", "status": 500})

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
        # Validate user inputs
        if not validator.validate_player_name(name):
            response = json.dumps({"response": "Invalid name", "status": 400})
        elif not validator.validate_score(score):
            response = json.dumps({"response": "Invalid score", "status": 400})

        else:  # If validation is successful
            lobby_id = service.create_lobby(rules)
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
        response = json.dumps({"response": "An error has occurred", "status": 500})

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
        # Validate user inputs
        if not validator.validate_lobby_id(lobby_id):
            response = json.dumps({"response": "Invalid lobby ID", "status": 400})
        elif not validator.validate_player_name(name):
            response = json.dumps({"response": "Invalid name", "status": 400})
        elif not validator.validate_score(score):
            response = json.dumps({"response": "Invalid score", "status": 400})

        else:  # If validation is successful
            rules = service.get_lobby_rules(lobby_id)
            if rules == "":  # if the lobby does not exist
                response = json.dumps(
                    {
                        "response": f"The lobby {lobby_id} does not exist",
                        "status": 400,
                    }
                )
            else:
                # Check whether the player already exists in the lobby
                player_id = service.get_player_id(lobby_id, name)
                if (
                    player_id == ""
                ):  # If the player does not have an ID, create a new one
                    player_id = service.create_player_data(
                        lobby_id, name, score, guessed_flights, rules
                    )

                # Get the latest scores for players in the lobby
                lobby_data = service.get_lobby_scores(lobby_id)

                response = json.dumps(
                    {
                        "response": {"player_id": player_id, "lobby_data": lobby_data},
                        "status": 200,
                    }
                )

    except:
        response = json.dumps({"response": "An error has occurred", "status": 500})

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
        # Validate user inputs
        if not validator.validate_lobby_id(lobby_id):
            response = json.dumps({"response": "Invalid lobby ID", "status": 400})

        else:  # If validation is successful
            lobby_data = service.get_lobby_scores(lobby_id)
            response = json.dumps({"response": lobby_data, "status": 200})

    except:
        response = json.dumps({"response": "An error has occurred", "status": 500})

    return response
