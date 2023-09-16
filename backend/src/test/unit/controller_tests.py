"""Unit tests for the controller functions"""

import json
import pytest
from unittest import mock
from src.service import controller, error_handling


class Flight:
    """mock of a FlightRadar24 Flight object used for testing"""

    def __init__(self):
        self.id = "test_id"
        self.origin_airport_name = "test_origin"
        self.destination_airport_name = "test_destination"
        self.aircraft_code = "test_aircraft"

    def set_flight_details(self, details):
        self.details = details


@pytest.fixture
def mock_flight():
    return Flight()


def test_get_airports_success(mocker):
    """
    Test the response and function calls for the get_airports controller
    function when the request is successful
    """
    mocker.patch.object(controller.service, "get_airports")
    controller.service.get_airports.return_value = ["name 1", "name 2", "name 3"]

    response = controller.get_airports()

    assert response == json.dumps(
        {"response": ["name 1", "name 2", "name 3"], "status": 200}
    )
    controller.service.get_airports.assert_called_once()


def test_get_airports_failure(mocker):
    """
    Test the response and function calls for the get_airports controller
    function when the request is unsuccessful
    """
    mocker.patch.object(controller.service, "get_airports")
    controller.service.get_airports.side_effect = Exception("test_error")

    response = controller.get_airports()

    assert response == json.dumps(
        {"response": "The server was unable to process your request", "status": 500}
    )
    controller.service.get_airports.assert_called_once()


@pytest.mark.parametrize("player_id", ["test_player_id", ""])
def test_handle_turn_success(mocker, mock_flight, player_id):
    """
    Test the response from the handle_turn controller function when the request
    is successful
    """
    test_longitude = "10.000"
    test_latitude = "5.0000"
    test_origin = "test_origin"
    test_destination = "test_destination"
    test_player_id = "test_player_id"

    mocker.patch.object(controller.service, "get_player_data")
    controller.service.get_player_data.return_value = ("123,456", 1)
    mocker.patch.object(controller.service, "get_closest_flight")
    controller.service.get_closest_flight.return_value = mock_flight
    mocker.patch.object(controller.service, "get_score")
    controller.service.get_score.return_value = "mock_score"
    mocker.patch.object(controller.service, "update_player_data")

    mocker.patch.object(controller.validator, "validate_position")
    mocker.patch.object(controller.validator, "validate_airport_names")
    mocker.patch.object(controller.validator, "validate_player_id")

    response = controller.handle_turn(
        test_longitude, test_latitude, test_origin, test_destination, test_player_id
    )

    assert response == json.dumps(
        {
            "response": {
                "id": "test_id",
                "origin": "test_origin",
                "destination": "test_destination",
                "aircraft": "test_aircraft",
                "score": "mock_score",
            },
            "status": 200,
        }
    )


def test_handle_turn_no_flights(mocker):
    """
    Test the response and function calls for the handle_turn controller
    function when no flights are found nearby
    """
    test_longitude = "10.000"
    test_latitude = "5.0000"
    test_origin = "test_origin"
    test_destination = "test_destination"
    test_player_id = "test_player_id"

    mocker.patch.object(controller.service, "get_player_data")
    controller.service.get_player_data.return_value = ("123,456", 1)
    mocker.patch.object(controller.service, "get_closest_flight")
    controller.service.get_closest_flight.return_value = None
    mocker.patch.object(controller.service, "get_score")
    controller.service.get_score.return_value = "mock_score"
    mocker.patch.object(controller.service, "update_player_data")

    mocker.patch.object(controller.validator, "validate_position")
    mocker.patch.object(controller.validator, "validate_airport_names")
    mocker.patch.object(controller.validator, "validate_player_id")

    response = controller.handle_turn(
        test_longitude, test_latitude, test_origin, test_destination, test_player_id
    )

    assert response == json.dumps({"response": "No flights were found", "status": 400})


def test_handle_turn_invalid_input(mocker, mock_flight):
    """
    Test the response from the handle_turn controller function when the request
    is unsuccessful due to an invalid user input.
    """
    test_longitude = "10.000"
    test_latitude = "5.0000"
    test_origin = "test_origin"
    test_destination = "test_destination"
    test_player_id = "test_player_id"

    mocker.patch.object(controller.service, "get_player_data")
    controller.service.get_player_data.return_value = ("123,456", 1)
    mocker.patch.object(controller.service, "get_closest_flight")
    controller.service.get_closest_flight.return_value = None
    mocker.patch.object(controller.service, "get_score")
    controller.service.get_score.return_value = "mock_score"
    mocker.patch.object(controller.service, "update_player_data")

    mocker.patch.object(controller.validator, "validate_position")
    controller.validator.validate_position.side_effect = (
        error_handling.ValidationException("test_error")
    )
    mocker.patch.object(controller.validator, "validate_airport_names")
    mocker.patch.object(controller.validator, "validate_player_id")

    response = controller.handle_turn(
        test_longitude, test_latitude, test_origin, test_destination, test_player_id
    )

    assert response == json.dumps({"response": "test_error", "status": 400})


def test_handle_turn_unsuccessful(mocker, mock_flight):
    """
    Test the response from the handle_turn controller function when the request
    is unsuccessful due to an unhandled runtime error.
    """
    test_longitude = "10.000"
    test_latitude = "5.0000"
    test_origin = "test_origin"
    test_destination = "test_destination"
    test_player_id = "test_player_id"

    mocker.patch.object(controller.service, "get_player_data")
    controller.service.get_player_data.side_effect = Exception("test_error")
    mocker.patch.object(controller.service, "get_closest_flight")
    controller.service.get_closest_flight.return_value = None
    mocker.patch.object(controller.service, "get_score")
    controller.service.get_score.return_value = "mock_score"
    mocker.patch.object(controller.service, "update_player_data")

    mocker.patch.object(controller.validator, "validate_position")
    mocker.patch.object(controller.validator, "validate_airport_names")
    mocker.patch.object(controller.validator, "validate_player_id")

    response = controller.handle_turn(
        test_longitude, test_latitude, test_origin, test_destination, test_player_id
    )

    assert response == json.dumps(
        {"response": "The server was unable to process your request", "status": 500}
    )


def test_create_lobby(mocker):
    """
    Test the response from the create_lobby controller function when the
    request is successful
    """
    name = "Mike Wazowski"
    score = "123"
    guessed_flights = "123,456,789"
    rules = 1

    mocker.patch.object(controller.service, "create_lobby")
    controller.service.create_lobby.return_value = "ABCD"
    mocker.patch.object(controller.service, "create_player_data")
    controller.service.create_player_data.return_value = "345"

    mocker.patch.object(controller.validator, "validate_player_name")
    mocker.patch.object(controller.validator, "validate_score")

    response = controller.create_lobby(name, score, guessed_flights, rules)

    assert response == json.dumps(
        {
            "response": {
                "lobby_id": "ABCD",
                "player_id": "345",
                "lobby_data": str([{"name": name, "player_id": "345", "score": score}]),
            },
            "status": 200,
        }
    )


def test_join_lobby_success(mocker):
    """
    Test the response from the join_lobby controller function when the
    request is successful
    """
    lobby_id = "ABCD"
    name = "Mike Wazowski"
    score = "123"
    guessed_flights = "123,456,789"

    mocker.patch.object(controller.service, "get_lobby_rules")
    controller.service.get_lobby_rules.return_value = 1
    mocker.patch.object(controller.service, "get_player_id")
    controller.service.get_player_id.return_value = "123-456-789"
    mocker.patch.object(controller.service, "create_player_data")
    controller.service.create_player_data.return_value = "345"
    mocker.patch.object(controller.service, "get_lobby_scores")
    controller.service.get_lobby_scores.return_value = [
        {"name": name, "player_id": "345", "score": score}
    ]

    mocker.patch.object(controller.validator, "validate_player_name")
    mocker.patch.object(controller.validator, "validate_score")

    response = controller.join_lobby(lobby_id, name, score, guessed_flights)

    assert response == json.dumps(
        {
            "response": {
                "player_id": "123-456-789",
                "lobby_data": [{"name": name, "player_id": "345", "score": score}],
                "rules": 1,
            },
            "status": 200,
        }
    )


def test_join_lobby_unsuccessful(mocker):
    """
    Test the response from the join_lobby controller function when the
    requested lobby does not exist
    """
    lobby_id = "ABCE"
    name = "Mike Wazowski"
    score = "123"
    guessed_flights = "123,456,789"

    mocker.patch.object(controller.service, "get_lobby_rules")
    controller.service.get_lobby_rules.return_value = ""
    mocker.patch.object(controller.service, "get_player_id")
    controller.service.get_player_id.return_value = "123-456-789"
    mocker.patch.object(controller.service, "create_player_data")
    controller.service.create_player_data.return_value = "345"
    mocker.patch.object(controller.service, "get_lobby_scores")
    controller.service.get_lobby_scores.return_value = [
        {"name": name, "player_id": "345", "score": score}
    ]

    mocker.patch.object(controller.validator, "validate_player_name")
    mocker.patch.object(controller.validator, "validate_score")

    response = controller.join_lobby(lobby_id, name, score, guessed_flights)

    assert response == json.dumps(
        {
            "response": f"The lobby {lobby_id} does not exist",
            "status": 400,
        }
    )


def test_get_lobby_scores_success(mocker):
    """
    Test the response from the get_lobby_scores controller function when
    the request is successful
    """
    lobby_id = "ABCD"

    lobby_data = [{"name": "Mike Wazowski", "player_id": "345", "score": "100"}]

    mocker.patch.object(controller.service, "get_lobby_scores")
    controller.service.get_lobby_scores.return_value = lobby_data

    mocker.patch.object(controller.validator, "validate_lobby_id")

    response = controller.get_lobby_scores(lobby_id)

    assert response == json.dumps({"response": lobby_data, "status": 200})


def test_get_lobby_scores_unsuccessful(mocker):
    """
    Test the response from the get_lobby_scores controller function when
    the requested lobby does not exist
    """
    lobby_id = "ABCE"

    mocker.patch.object(controller.service, "get_lobby_scores")
    controller.service.get_lobby_scores.return_value = "[]"

    mocker.patch.object(controller.validator, "validate_lobby_id")

    response = controller.get_lobby_scores(lobby_id)

    assert response == json.dumps({"response": "Lobby not found", "status": 404})
