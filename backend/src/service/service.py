"""Core functionality of the application"""

import os
import random
import string
import uuid
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import boto3
from boto3.dynamodb.conditions import Attr
from FlightRadar24.api import FlightRadar24API

fr_api = FlightRadar24API()

table_name = os.getenv("GAME_DATA_TABLE", None)
dynamoClient = boto3.client("dynamodb")


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


def get_score(flight, origin, destination):
    """
    Function to evaluate the points earned from a destination guess

    Args:
        flight [FlightRadar24 Flight]: flight to check
        origin [string]: origin airport guess
        destination [string]: destination airport guess

    Returns:
        integer: points awarded
    """

    score = 0
    airport_list = None

    # Origin Guess
    if origin != "":
        if flight.origin_airport_name == origin:
            # in the case of a perfect match, gain 100 points
            score += 100
        else:
            # else find the distance between the guess and the correct airport
            # and convert this into a score
            if airport_list is None:
                airport_list = pd.DataFrame(fr_api.get_airports())
                # Remove any escape characters
                airport_list["name"] = remove_escape_characters(
                    airport_list.loc[:, "name"].to_list()
                )

            airport_data = airport_list[
                (airport_list["name"] == origin)
                | (airport_list["name"] == flight.origin_airport_name)
            ]
            distance = np.sqrt(
                pow(airport_data["lat"].iloc[0] - airport_data["lat"].iloc[1], 2)
                + pow(airport_data["lon"].iloc[0] - airport_data["lon"].iloc[1], 2)
            )
            score += max(np.floor(100 - 4 * pow(distance, 3)), 0)

    # Destination Guess
    if destination != "":
        if flight.destination_airport_name == destination:
            # in the case of a perfect match, gain 100 points
            score += 100
        else:
            # else find the distance between the guess and the correct airport
            # and convert this into a score
            if airport_list is None:
                airport_list = pd.DataFrame(fr_api.get_airports())
                # Remove any escape characters
                airport_list["name"] = remove_escape_characters(
                    airport_list.loc[:, "name"].to_list()
                )

            airport_data = airport_list[
                (airport_list["name"] == destination)
                | (airport_list["name"] == flight.destination_airport_name)
            ]
            distance = np.sqrt(
                pow(airport_data["lat"].iloc[0] - airport_data["lat"].iloc[1], 2)
                + pow(airport_data["lon"].iloc[0] - airport_data["lon"].iloc[1], 2)
            )
            score += max(np.floor(100 - 4 * pow(distance, 3)), 0)

    return score


def get_unique_lobby_id():
    """
    Generates a unique four-letter code to identify a lobby.

    Returns:
        string: Lobby ID
    """

    unique = False

    # while not unique:
    lobby_id = "".join(random.choice(string.ascii_uppercase) for i in range(4))
    if (
        dynamoClient.scan(
            TableName=table_name, FilterExpression=Attr("lobby_id").eq(lobby_id)
        )["Count"]
        == 0
    ):
        unique = True

    return lobby_id


def create_player_data(lobby_id, name, score):
    """
    Generates a unique ID to identify a player, and creates a record in the
    dynamo table corresponding to the player.

    Returns:
        string: Player ID
    """

    player_id = str(uuid.uuid4())

    dynamoClient.put_item(
        TableName=table_name,
        Item={
            "player_id": player_id,
            "lobby_id": lobby_id,
            "player_name": name,
            "score": int(score),
            "last_interaction": datetime.now().strftime("%Y-%m-%d %H:%M"),
        },
    )

    return player_id


def get_player_id(lobby_id, name):
    """
    Checks by name whether a player exists within a given lobby.
    If so, the function will return their existing player_id.
    Otherwise the function will generate a player_id for the player.

    Returns:
        string: If the player already exists, this will be their Unique
                Player ID, otherwise this will be an empty string.
    """

    scan_response = dynamoClient.scan(
        TableName=table_name,
        FilterExpression=Attr("lobby_id").eq(lobby_id) & Attr("name").eq(name),
    )
    result = (
        "" if scan_response["Count"] == 0 else scan_response["Items"][0]["player_id"]
    )

    return result


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
    scan_response = dynamoClient.scan(
        TableName=table_name, FilterExpression=Attr("lobby_id").eq(lobby_id)
    )["Items"]

    for entry in scan_response:
        lobby_data = np.append(
            lobby_data, {"name": entry["name"], "score": int(entry["score"])}
        )

    lobby_data = str(lobby_data)  # string type allows for json serialization

    return lobby_data


def update_player_score(player_id, score):
    """
    Adds a given number of points to a player's score in the dynamo table.

    Args:
        player_id [string]: ID of the player
        score [integer]: Points to add to the player's score
    """

    dynamoClient.update_item(
        TableName=table_name,
        Key={"player_id": player_id},
        UpdateExpression="SET score = score + :val",
        ExpressionAttributeValues={":val": score},
    )


def delete_lobby():
    """
    Deletes data older than one day from the dynamo table.
    """

    scan_response = dynamoClient.scan(TableName=table_name)["Items"]

    for entry in scan_response:
        date = datetime(
            year=entry["last_interaction"][:4],
            month=entry["last_interaction"][5:7],
            day=entry["last_interaction"][8:10],
            hour=entry["last_interaction"][11:13],
            minute=entry["last_interaction"][14:],
        )

        if date < datetime.now() - timedelta(days=1):
            dynamoClient.delete_item(
                TableName=table_name, Key={"player_id": entry["player_id"]}
            )


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
