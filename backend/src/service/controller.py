"""Controllers for AWS Lambda functions"""

import json
from src.service import service, validator
from src.service.error_handling import ValidationException, handle_exceptions


@handle_exceptions
def get_airports():
    """
    Controller for the get_airports Lambda function, which returns a
    complete list of airport names.

    Returns a json object with:
        "response": a list of airport names
        "status": request status code
    """

    airport_names = service.get_airports()
    response = json.dumps({"response": airport_names, "status": 200})

    return response


@handle_exceptions
def handle_turn(longitude, latitude, origin, destination, player_id):
    """
    Controller for the handle_turn Lambda function, which returns data
    corresponding to the closest flight to a provided longitude-latitude
    pair along with a score based on the proximity of a destination guess.
    If a player_id is provided, the player table will be updated to reflect
    any points scored.

    Args:
        longitude [string]: longitude to search from
        latitude [string]: latitude to search from
        origin [string]: origin airport guess
        destination [string]: destination airport guess
        player_id [string]: ID of the player (optional)

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

    validator.validate_position(longitude, latitude)
    validator.validate_airport_names(origin, destination)

    player_is_in_lobby = player_id != ""
    if player_is_in_lobby:
        validator.validate_player_id(player_id)
        guessed_flights, rules = service.get_player_data(player_id)
    else:
        rules = None

    flight = service.get_closest_flight(float(longitude), float(latitude))
    if flight is None:
        raise ValidationException("No flights were found")

    if player_is_in_lobby:
        flight_already_guessed = flight.id in guessed_flights.split(",")
        if flight_already_guessed:
            raise ValidationException("You have already made a guess for this flight")

    score = service.get_score(flight, origin, destination, rules)

    if player_is_in_lobby:
        service.update_player_data(player_id, score, flight.id, guessed_flights)

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

    return response


@handle_exceptions
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

    # Validate user inputs
    validator.validate_player_name(name)
    validator.validate_score(score)

    lobby_id = service.create_lobby(rules)
    player_id = service.create_player_data(lobby_id, name, score, guessed_flights)
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

    return response


@handle_exceptions
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
            "rules": enum of the ruleset of the lobby
            "lobby_data": [{"name": string, "score": string}, ...]
        "status": request status code
    """

    # Validate user inputs
    validator.validate_lobby_id(lobby_id)
    validator.validate_player_name(name)
    validator.validate_score(score)

    rules = service.get_lobby_rules(lobby_id)
    if rules == "":  # if the lobby does not exist
        raise ValidationException(f"The lobby {lobby_id} does not exist")

    # Check whether the player already exists in the lobby
    player_id = service.get_player_id(lobby_id, name)
    if player_id == "":
        # If the player does not have an ID then generate one
        player_id = service.create_player_data(lobby_id, name, score, guessed_flights)

    # Get the latest scores for players in the lobby
    lobby_data = service.get_lobby_scores(lobby_id)

    response = json.dumps(
        {
            "response": {
                "player_id": player_id,
                "lobby_data": lobby_data,
                "rules": rules,
            },
            "status": 200,
        }
    )

    return response


@handle_exceptions
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

    # Validate user inputs
    validator.validate_lobby_id(lobby_id)

    lobby_data = service.get_lobby_scores(lobby_id)

    if lobby_data == "[]":
        response = json.dumps({"response": "Lobby not found", "status": 404})
    else:
        response = json.dumps({"response": lobby_data, "status": 200})

    return response
