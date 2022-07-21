"""Core functionality of the application"""

import numpy as np
import pandas as pd
from FlightRadar24.api import FlightRadar24API

fr_api = FlightRadar24API()


def get_airports():
    """
    Function to get a complete list of airports

    Returns:
        string[]: Airport names
    """

    airports = fr_api.get_airports()
    airport_data = pd.DataFrame(airports)
    airport_names = airport_data.loc[:, "name"].to_list()
    return airport_names


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


def get_score(flight, airport):
    """
    Function to evaluate the points earned from a desination guess

    Args:
        flight [FlightRadar24 Flight]: flight to check
        airport [string]: destination airport guess

    Returns:
        integer: points awarded
    """

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
        score = max(np.floor(100 - 4 * pow(distance, 3)), 0)

    return score
