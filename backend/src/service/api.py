"""Handlers for AWS Lambda functions"""

import json
from src.service import controller


def get_airports(event, context):
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


def handle_turn(event, context):
    """
    Handler for the handle_turn Lambda function, which returns data
    corresponding to the closest flight to a provided longitude-latitude
    pair along with a score based on the proximity of a destination guess.

    Args:
        event: AWS Lambda event. "body" should be a json string containing
               "longitude", "latitude", and "airport".
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
    longitude = float(body.get("longitude"))
    latitude = float(body.get("latitude"))
    airport = body.get("airport")

    response = controller.handle_turn(longitude, latitude, airport)

    return response
