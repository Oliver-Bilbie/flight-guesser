"""unit tests for the core functions"""

import numpy as np
from unittest import mock
from src.service import service


class Flight:
    """mock of a FlightRadar24 Flight object used for testing"""

    def __init__(self):
        self.id = "test_id"
        self.origin_airport_name = "test_airport"
        self.destination_airport_name = "test_airport_2"
        self.aircraft_code = "test_aircraft"

    def set_flight_details(self, details):
        self.details = details


airport_data = [
    {
        "name": "test_airport",
        "iata": "QWE",
        "icao": "ASDF",
        "lat": 0,
        "lon": 0,
        "country": "Kenya",
        "alt": 5532,
    },
    {
        "name": "test_airport_2",
        "iata": "RTY",
        "icao": "GHJK",
        "lat": 1,
        "lon": 1,
        "country": "Spain",
        "alt": 326,
    },
    {
        "name": "test_airport_3",
        "iata": "UIO",
        "icao": "ZXCV",
        "lat": -2.5,
        "lon": 2,
        "country": "Germany",
        "alt": 623,
    },
]


def test_get_airports(mocker):
    """test the response and function calls for the get_airports service function"""
    mocker.patch.object(service.fr_api, "get_airports")
    service.fr_api.get_airports.return_value = airport_data

    mocker.patch.object(service, "remove_escape_characters")
    service.remove_escape_characters.return_value = [
        "test_airport_4",
        "test_airport_5",
        "test_airport_6",
    ]

    response = service.get_airports()

    assert response == [
        "test_airport_4",
        "test_airport_5",
        "test_airport_6",
    ]
    service.fr_api.get_airports.assert_called_once()
    service.remove_escape_characters.assert_called_once_with(
        [
            "test_airport",
            "test_airport_2",
            "test_airport_3",
        ]
    )


def test_get_closest_flight(mocker):
    """test the response and function calls for the get_closest_flight service function when the request is successful"""
    test_longitude = 1
    test_latitude = 2
    mock_flight = Flight()

    mocker.patch.object(service.fr_api, "get_flights")
    service.fr_api.get_flights.return_value = [mock_flight]

    mocker.patch.object(service.fr_api, "get_flight_details")
    service.fr_api.get_flight_details.return_value = "details"

    response = service.get_closest_flight(test_longitude, test_latitude)

    assert response.id == "test_id"
    assert response.origin_airport_name == "test_airport"
    assert response.destination_airport_name == "test_airport_2"
    assert response.aircraft_code == "test_aircraft"
    assert response.details == "details"

    service.fr_api.get_flights.assert_called_once_with(bounds="2.01,1.99,0.99,1.01")
    service.fr_api.get_flight_details.assert_called_once_with("test_id")


def test_get_closest_flight_no_flights(mocker):
    """test the response and function calls for the get_closest_flight service function when no flights are found nearby"""
    test_longitude = 1
    test_latitude = 2

    mocker.patch.object(service.fr_api, "get_flights")
    service.fr_api.get_flights.return_value = []

    response = service.get_closest_flight(test_longitude, test_latitude)

    assert response == None
    assert service.fr_api.get_flights.call_count == 49


def test_get_score_both_perfect(mocker):
    """test the response and function calls for the get_score service function when the guess matches the destination"""
    test_flight = Flight()
    test_origin = "test_airport"
    test_destination = "test_airport_2"

    mocker.patch.object(service.fr_api, "get_airports")
    service.fr_api.get_airports.return_value = airport_data

    response = service.get_score(test_flight, test_origin, test_destination)

    assert response == 200
    service.fr_api.get_airports.assert_not_called()


def test_get_score_origin_perfect(mocker):
    """test the response and function calls for the get_score service function when the guess matches the destination"""
    test_flight = Flight()
    test_origin = "test_airport"
    test_destination = "test_airport_3"

    mocker.patch.object(service.fr_api, "get_airports")
    service.fr_api.get_airports.return_value = airport_data

    response = service.get_score(test_flight, test_origin, test_destination)

    assert response == 100
    service.fr_api.get_airports.assert_called_once()


def test_get_score_destination_perfect(mocker):
    """test the response and function calls for the get_score service function when the guess matches the destination"""
    test_flight = Flight()
    test_origin = "test_airport_3"
    test_destination = "test_airport_2"

    mocker.patch.object(service.fr_api, "get_airports")
    service.fr_api.get_airports.return_value = airport_data

    response = service.get_score(test_flight, test_origin, test_destination)

    assert response == 100
    service.fr_api.get_airports.assert_called_once()


def test_get_score_both_close(mocker):
    """test the response and function calls for the get_score service function when the guess is close enough to the desination to score points"""
    test_flight = Flight()
    test_origin = "test_airport_2"
    test_destination = "test_airport"

    mocker.patch.object(service.fr_api, "get_airports")
    service.fr_api.get_airports.return_value = airport_data

    response = service.get_score(test_flight, test_origin, test_destination)

    assert response == 176.0
    service.fr_api.get_airports.assert_called_once()


def test_get_score_far(mocker):
    """test the response and function calls for the get_score service function when the guess is too far from the desination to score points"""
    test_flight = Flight()
    test_origin = "test_airport_3"
    test_destination = "test_airport_3"

    mocker.patch.object(service.fr_api, "get_airports")
    service.fr_api.get_airports.return_value = airport_data

    response = service.get_score(test_flight, test_origin, test_destination)

    assert response == 0
    service.fr_api.get_airports.assert_called_once()


def test_remove_escape_characters():
    """test the response for the remove_escape_characters service function"""
    escape_chars = ["\t", "\b", "\n", "\r", "\f"]
    items = ["item1", "item2", "item3", "item4", "item5"]

    test_items = test_items = np.core.defchararray.add(escape_chars, items)

    assert (service.remove_escape_characters(test_items) == items).all()
