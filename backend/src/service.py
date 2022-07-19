import json
import numpy as np
import pandas as pd
from FlightRadar24.api import FlightRadar24API

fr_api = FlightRadar24API()


def get_airports(event, context):
    try:
        airports = fr_api.get_airports()
        airport_data = pd.DataFrame(airports)
        airport_names = airport_data.loc[:, "name"].to_list()
        response = json.dumps({"response": airport_names, "status": 200})

    except:
        response = json.dumps({"response": "An error has occurred.", "status": 500})

    return response


def get_closest_flight(x, y):
    flights = []
    radius = 0.05

    while len(flights) == 0 and radius <= 0.5:
        bounds = f"{y+radius},{y-radius},{x-radius},{x+radius}"
        flights = fr_api.get_flights(bounds=bounds)
        radius += 0.01

    if len(flights) == 0:
        flight = None
    else:
        flight = flights[0]
        details = fr_api.get_flight_details(flight.id)
        flight.set_flight_details(details)

    return flight


def get_score(flight, airport):
    if flight.destination_airport_name == airport:
        # in the case of a perfect match, gain 100 points
        score = 100
    else:
        # else find the distance between the guess and the correct airport
        # and convert this into a score
        airport_data = pd.DataFrame(fr_api.get_airports())
        airport_data = airport_data[
            (airport_data["name"] == airport)
            | (airport_data["name"] == flight.destination_airport_name)
        ]
        distance = np.sqrt(
            pow(airport_data["lat"].iloc[0] - airport_data["lat"].iloc[1], 2)
            + pow(airport_data["lon"].iloc[0] - airport_data["lon"].iloc[1], 2)
        )
        score = np.floor(100 - 4 * pow(distance, 3))
        if score < 0:
            score = 0

    return score


def handle_turn(event, context):
    try:
        body = event.get("body")
        body = json.loads(body)
        x = float(body.get("x"))
        y = float(body.get("y"))
        airport = body.get("airport")

        flight = get_closest_flight(x, y)

        if flight == None:
            response = json.dumps({"response": "No flights were found", "status": 400})
        else:
            score = get_score(flight, airport)

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
