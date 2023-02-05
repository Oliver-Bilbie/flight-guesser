"""Core functionality of the application"""

import os
import random
import string
import uuid
from decimal import Decimal
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import boto3
from boto3.dynamodb.conditions import Attr, Key
from FlightRadar24.api import FlightRadar24API

fr_api = FlightRadar24API()

lobbyTableName = os.getenv("LOBBY_DATA_TABLE", None)
playerTableName = os.getenv("PLAYER_DATA_TABLE", None)

dynamoResource = boto3.resource("dynamodb")
lobbyTable = dynamoResource.Table(lobbyTableName) if lobbyTableName else None
playerTable = dynamoResource.Table(playerTableName) if playerTableName else None


def get_airports():
    """
    Function to get a complete list of airports

    Returns:
        string[]: Airport names
    """

    # Get data from FR API
    airports = fr_api.get_airports()

    airport_data = pd.DataFrame(airports)
    airport_names = airport_data.loc[:, "name"].to_list()

    # Remove escape characters
    airport_names = remove_escape_characters(airport_names)

    # Sort alphabetically
    airport_names = np.sort(airport_names)

    return airport_names.tolist()


def get_closest_flight(longitude, latitude):
    """
    Function to get the details of the closest flight to a given location

    Args:
        longitude [float]: longitude to search from
        latitude [float]: latitude to search from

    Returns:
        FlightRadar24 Flight: closest flight
    """

    flights = []
    radius = 0.01

    while len(flights) == 0 and radius <= 0.5:
        bounds = (
            f"{latitude+radius},{latitude-radius},{longitude-radius},{longitude+radius}"
        )
        flights = fr_api.get_flights(bounds=bounds)
        radius += 0.01

    if len(flights) == 0:
        flight = None
    else:
        flight = flights[0]
        details = fr_api.get_flight_details(flight.id)
        flight.set_flight_details(details)

    return flight


def get_score(flight, origin, destination, rules):
    """
    Function to evaluate the points earned from a guess

    Args:
        flight [FlightRadar24 Flight]: flight to check
        origin [string]: origin airport guess
        destination [string]: destination airport guess
        rules [integer]: Integer encoded ruleset of the lobby

    Returns:
        integer: points awarded
    """

    score = 0
    airport_list = None

    guessed_locations = []
    correct_locations = []

    # If the player is not in a multiplayer lobby, we will check any provided guesses
    if rules is None:
        if origin != "":
            guessed_locations.append(origin)
            correct_locations.append(flight.origin_airport_name)
        if destination != "":
            guessed_locations.append(destination)
            correct_locations.append(flight.destination_airport_name)

    # If the player is in a multiplayer lobby, we will only check guesses permitted
    # by the lobby rules
    else:
        if rules % 2 == 1:
            guessed_locations.append(origin)
            correct_locations.append(flight.origin_airport_name)
        if rules // 2 == 1:
            guessed_locations.append(destination)
            correct_locations.append(flight.destination_airport_name)

    for index in range(len(guessed_locations)):
        if guessed_locations[index] != "":
            if correct_locations[index] == guessed_locations[index]:
                # in the case of a perfect match, gain 100 points
                score += 100

            else:
                # else find the distance between the guess and the correct airport
                # and convert this into a score

                # avoid reloading the airport list if it has already been fetched
                if airport_list is None:
                    # Load airport data from the flight radar API
                    airport_list = pd.DataFrame(fr_api.get_airports())
                    # Remove any escape characters
                    airport_list["name"] = remove_escape_characters(
                        airport_list.loc[:, "name"].to_list()
                    )

                airport_data = airport_list[
                    (airport_list["name"] == guessed_locations[index])
                    | (airport_list["name"] == correct_locations[index])
                ]

                distance = evaluate_distance(
                    airport_data["lon"].iloc[0],
                    airport_data["lat"].iloc[0],
                    airport_data["lon"].iloc[1],
                    airport_data["lat"].iloc[1],
                )

                score += np.floor(100 * np.exp(-distance / 250))

    return score


def evaluate_distance(from_longitude, from_latitude, to_longitude, to_latitude):
    """
    Calcuates the distance between two locations defined using longitude and latitude pairs.
    For simplicity it is assumed that the Earth is a perfect sphere.

    Args:
        from_longitude [Float]: Longitude value of the first coordinate in degrees
        from_latitude [Float]: Latitude value of the first coordinate in degrees
        to_longitude [Float]: Longitude value of the second coordinate in degrees
        to_latitude [Float]: Latitude value of the second coordinate in degrees

    Returns:
        Float: Separation distance in km
    """

    radius = 6378.137  # Equatorial radius of the Earth in km (source: NASA)

    # Convert angles from degrees to radians
    from_longitude *= np.pi / 180
    from_latitude *= np.pi / 180
    to_longitude *= np.pi / 180
    to_latitude *= np.pi / 180

    distance = radius * np.arccos(
        np.cos(to_latitude - from_latitude)
        - np.cos(to_latitude)
        * np.cos(from_latitude)
        * (1 - np.cos(to_longitude - from_longitude))
    )

    return distance


def create_lobby(rules):
    """
    Generates a unique four-letter code to identify a lobby and creates a corresponding entry in the lobby table.

    Args:
        rules [integer]: Integer encoded ruleset of the lobby

    Returns:
        string: Lobby ID
    """

    unique = False

    while not unique:
        # Generate a random four-letter string
        lobby_id = "".join(random.choice(string.ascii_uppercase) for i in range(4))

        # Confirm that this lobby ID is not already in use
        if (
            lobbyTable.query(KeyConditionExpression=Key("lobby_id").eq(lobby_id))[
                "Count"
            ]
            == 0
        ):
            unique = True

    lobbyTable.put_item(
        Item={
            "lobby_id": lobby_id,
            "rules": rules,
            "last_interaction": datetime.now().strftime("%Y-%m-%d %H:%M"),
        },
    )

    return lobby_id


def get_player_id(lobby_id, name):
    """
    Checks by name whether a player exists within a given lobby.
    If so, the function will return their existing player_id.
    Otherwise the function will generate a player_id for the player.

    Args:
        lobby_id [string]: ID of the lobby
        name [string]: Name of the player

    Returns:
        string: If the player already exists, this will be their Unique
                Player ID, otherwise this will be an empty string.
    """

    query_response = playerTable.query(
        KeyConditionExpression=Key("lobby_id").eq(lobby_id)
        & Key("player_name").eq(name),
        IndexName="LobbyIndex",
    )

    result = (
        "" if query_response["Count"] == 0 else query_response["Items"][0]["player_id"]
    )

    return result


def get_lobby_rules(lobby_id):
    """
    Returns an integer corresponding to the specified lobby's rules.

    Args:
        lobby_id [string]: ID of the lobby

    Returns:
        string: Integer-encoded lobby rules, or an empty string if the lobby does not exist
    """

    query_response = lobbyTable.get_item(Key={"lobby_id": lobby_id})

    rules = (
        ""
        if query_response.get("Item") is None
        else int(query_response.get("Item").get("rules"))
    )

    return rules


def get_lobby_scores(lobby_id):
    """
    Returns the a list containing the names and scores of all members of
    a given lobby.

    Args:
        lobby_id [string]: ID of the lobby

    Returns:
        string: [{"name": string, "score": string}, ...]
    """

    lobby_data = []
    query_response = playerTable.query(
        KeyConditionExpression=Key("lobby_id").eq(lobby_id), IndexName="LobbyIndex"
    )["Items"]

    for entry in query_response:
        lobby_data = np.append(
            lobby_data,
            {
                "name": entry["player_name"],
                "player_id": entry["player_id"],
                "score": int(entry["score"]),
            },
        )

    lobby_data = str(lobby_data)  # string type allows for json serialization

    return lobby_data


def create_player_data(lobby_id, name, score, guessed_flights):
    """
    Generates a unique ID to identify a player, and creates a record in the
    dynamo table corresponding to the player.

    Args:
        lobby_id [string]: ID of the lobby
        name [string]: Name of the player
        score [string]: Score of the player
        guessed_flights [string[]]: Flight IDs previously guessed by the player

    Returns:
        string: Player ID
    """

    player_id = str(uuid.uuid4())

    playerTable.put_item(
        Item={
            "player_id": player_id,
            "lobby_id": lobby_id,
            "player_name": name,
            "score": int(score),
            "guessed_flights": guessed_flights,
            "last_interaction": datetime.now().strftime("%Y-%m-%d %H:%M"),
        },
    )

    return player_id


def get_player_data(player_id):
    """
    Retrieves the player data required for input validation from the dynamo tables.

    Args:
        player_id [string]: ID of the player

    Returns:
        string[]: Flight IDs previously guessed by the player
        integer: Integer encoded ruleset of the lobby
    """

    playerData = playerTable.get_item(Key={"player_id": player_id}).get("Item")

    lobby_id = playerData.get("lobby_id")
    guessed_flights = playerData.get("guessed_flights")
    rules = int(get_lobby_rules(lobby_id))

    return guessed_flights, rules


def update_player_data(player_id, score, flight_id, guessed_flights):
    """
    Adds a given number of points to a player's score and guessed flights in the dynamo table.

    Args:
        player_id [string]: ID of the player
        score [integer]: Points to add to the player's score
        flight_id [string]: ID of the most recently guessed flight
    """

    updated_guessed_flights = (
        f"{guessed_flights},{flight_id}" if guessed_flights != "" else flight_id
    )

    playerTable.update_item(
        Key={"player_id": player_id},
        UpdateExpression="SET score = score + :val, guessed_flights = :fid",
        ExpressionAttributeValues={
            ":val": Decimal(score),
            ":fid": updated_guessed_flights,
        },
    )


def delete_old_data():
    """
    Deletes data older than one day from the dynamo tables.
    """

    for table in [playerTable, lobbyTable]:
        scan_response = table.scan()["Items"]

        for entry in scan_response:
            date = datetime(
                year=int(entry["last_interaction"][:4]),
                month=int(entry["last_interaction"][5:7]),
                day=int(entry["last_interaction"][8:10]),
                hour=int(entry["last_interaction"][11:13]),
                minute=int(entry["last_interaction"][14:]),
            )

            if date < datetime.now() - timedelta(days=1):
                playerTable.delete_item(Key={"player_id": entry["player_id"]})


def remove_escape_characters(items):
    """
    Removes escape characters from a list of strings

    Args:
        items (string[]): Items to be cleaned

    Returns:
        string[]: Cleaned items
    """

    for esc_char in ["\t", "\b", "\n", "\r", "\f"]:
        items = np.char.replace(items, esc_char, "")

    return items
