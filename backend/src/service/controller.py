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


def handle_turn(longitude, latitude, origin, destination, data_saver):
    """
    Controller for the handle_turn Lambda function, which returns data
    corresponding to the closest flight to a provided longitude-latitude
    pair along with a score based on the proximity of a destination guess.

    Args:
        longitude [float]: longitude to search from
        latitude [float]: latitude to search from
        origin [string]: origin airport guess
        destination [string]: destination airport guess
        data_saver [string]: "y" or "n" corresponding to yes or no

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
