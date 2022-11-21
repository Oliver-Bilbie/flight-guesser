"""unit tests for the controller functions"""

from unittest import mock
from src.service import controller


class Flight:
    """mock of a FlightRadar24 Flight object used for testing"""

    def __init__(self):
        self.id = "test_id"
        self.origin_airport_name = "test_origin"
        self.destination_airport_name = "test_destination"
        self.aircraft_code = "test_aircraft"

    def set_flight_details(self, details):
        self.details = details


def test_get_airports_success(mocker):
    """test the response and function calls for the get_airports controller function when the request is successful"""
    mocker.patch.object(controller.service, "get_airports")
    controller.service.get_airports.return_value = ["name 1", "name 2", "name 3"]

    response = controller.get_airports()

    assert response == '{"response": ["name 1", "name 2", "name 3"], "status": 200}'
    controller.service.get_airports.assert_called_once()


def test_get_airports_failure(mocker):
    """test the response and function calls for the get_airports controller function when the request is unsuccessful"""
    mocker.patch.object(controller.service, "get_airports")
    controller.service.get_airports.side_effect = Exception("test_error")

    response = controller.get_airports()

    assert response == '{"response": "An error has occurred.", "status": 500}'
    controller.service.get_airports.assert_called_once()


def test_handle_turn_success(mocker):
    """test the response and function calls for the handle_turn controller function when the request is successful"""
    test_longitude = "10.000"
    test_latitude = "5.0000"
    test_origin = "test_origin"
    test_destination = "test_destination"
    test_player_id = "test_player_id"
    mock_flight = Flight()

    mocker.patch.object(controller.service, "get_closest_flight")
    controller.service.get_closest_flight.return_value = mock_flight
    mocker.patch.object(controller.service, "get_score")
    controller.service.get_score.return_value = "mock_score"
    mocker.patch.object(controller.service, "update_player_score")

    mocker.patch.object(controller.validator, "validate_position")
    controller.validator.validate_position.return_value = True
    mocker.patch.object(controller.validator, "validate_airport_names")
    controller.validator.validate_airport_names.return_value = True
    mocker.patch.object(controller.validator, "validate_player_id")
    controller.validator.validate_player_id.return_value = True

    response = controller.handle_turn(
        test_longitude, test_latitude, test_origin, test_destination, test_player_id
    )

    assert (
        response
        == '{"response": {"id": "test_id", "origin": "test_origin", "destination": "test_destination", "aircraft": "test_aircraft", "score": "mock_score"}, "status": 200}'
    )
    controller.service.get_closest_flight.assert_called_once_with(
        float(test_longitude), float(test_latitude)
    )
    controller.service.get_score.assert_called_once_with(
        mock_flight, test_origin, test_destination
    )
    controller.service.update_player_score.assert_called_once_with(
        test_player_id, "mock_score"
    )


def test_handle_turn_success_no_player_id(mocker):
    """test the response and function calls for the handle_turn controller function when the request is successful"""
    test_longitude = "10.000"
    test_latitude = "5.0000"
    test_origin = "test_origin"
    test_destination = "test_destination"
    test_player_id = ""
    mock_flight = Flight()

    mocker.patch.object(controller.service, "get_closest_flight")
    controller.service.get_closest_flight.return_value = mock_flight
    mocker.patch.object(controller.service, "get_score")
    controller.service.get_score.return_value = "mock_score"
    mocker.patch.object(controller.service, "update_player_score")

    mocker.patch.object(controller.validator, "validate_position")
    controller.validator.validate_position.return_value = True
    mocker.patch.object(controller.validator, "validate_airport_names")
    controller.validator.validate_airport_names.return_value = True
    mocker.patch.object(controller.validator, "validate_player_id")
    controller.validator.validate_player_id.return_value = True

    response = controller.handle_turn(
        test_longitude, test_latitude, test_origin, test_destination, test_player_id
    )

    assert (
        response
        == '{"response": {"id": "test_id", "origin": "test_origin", "destination": "test_destination", "aircraft": "test_aircraft", "score": "mock_score"}, "status": 200}'
    )
    controller.service.get_closest_flight.assert_called_once_with(
        float(test_longitude), float(test_latitude)
    )
    controller.service.get_score.assert_called_once_with(
        mock_flight, test_origin, test_destination
    )
    controller.service.update_player_score.assert_not_called()


def test_handle_turn_no_flights(mocker):
    """test the response and function calls for the handle_turn controller function when no flights are found nearby"""
    test_longitude = "10.000"
    test_latitude = "5.0000"
    test_origin = "test_origin"
    test_destination = "test_destination"
    test_player_id = "test_player_id"

    mocker.patch.object(controller.service, "get_closest_flight")
    controller.service.get_closest_flight.return_value = None
    mocker.patch.object(controller.service, "get_score")
    mocker.patch.object(controller.service, "update_player_score")

    mocker.patch.object(controller.validator, "validate_position")
    controller.validator.validate_position.return_value = True
    mocker.patch.object(controller.validator, "validate_airport_names")
    controller.validator.validate_airport_names.return_value = True
    mocker.patch.object(controller.validator, "validate_player_id")
    controller.validator.validate_player_id.return_value = True

    response = controller.handle_turn(
        test_longitude, test_latitude, test_origin, test_destination, test_player_id
    )

    assert response == '{"response": "No flights were found", "status": 400}'
    controller.service.get_closest_flight.assert_called_once_with(
        float(test_longitude), float(test_latitude)
    )
    controller.service.get_score.assert_not_called()


def test_handle_turn_failure(mocker):
    """test the response and function calls for the handle_turn controller function when the request is unsuccessful"""
    test_longitude = "10.000"
    test_latitude = "5.0000"
    test_origin = "test_origin"
    test_destination = "test_destination"
    test_player_id = "test_player_id"

    mocker.patch.object(controller.service, "get_closest_flight")
    controller.service.get_closest_flight.side_effect = Exception("test_error")
    mocker.patch.object(controller.service, "update_player_score")

    mocker.patch.object(controller.validator, "validate_position")
    controller.validator.validate_position.return_value = True
    mocker.patch.object(controller.validator, "validate_airport_names")
    controller.validator.validate_airport_names.return_value = True
    mocker.patch.object(controller.validator, "validate_player_id")
    controller.validator.validate_player_id.return_value = True

    response = controller.handle_turn(
        test_longitude, test_latitude, test_origin, test_destination, test_player_id
    )

    assert response == '{"response": "An error has occurred.", "status": 500}'
    controller.service.get_closest_flight.assert_called_once()


def test_handle_turn_invalid_position(mocker):
    """test the response and function calls for the handle_turn controller function when the request is unsuccessful"""
    test_longitude = "10.000"
    test_latitude = "5.0000"
    test_origin = "test_origin"
    test_destination = "test_destination"
    test_player_id = "test_player_id"
    mock_flight = Flight()

    mocker.patch.object(controller.service, "get_closest_flight")
    controller.service.get_closest_flight.return_value = mock_flight
    mocker.patch.object(controller.service, "get_score")
    controller.service.get_score.return_value = "mock_score"
    mocker.patch.object(controller.service, "update_player_score")

    mocker.patch.object(controller.validator, "validate_position")
    controller.validator.validate_position.return_value = False
    mocker.patch.object(controller.validator, "validate_airport_names")
    controller.validator.validate_airport_names.return_value = True
    mocker.patch.object(controller.validator, "validate_player_id")
    controller.validator.validate_player_id.return_value = True

    response = controller.handle_turn(
        test_longitude, test_latitude, test_origin, test_destination, test_player_id
    )

    assert response == '{"response": "Invalid position", "status": 400}'
    controller.service.get_closest_flight.assert_not_called()


def test_handle_turn_invalid_airport_names(mocker):
    """test the response and function calls for the handle_turn controller function when the request is unsuccessful"""
    test_longitude = "10.000"
    test_latitude = "5.0000"
    test_origin = "test_origin"
    test_destination = "test_destination"
    test_player_id = "test_player_id"
    mock_flight = Flight()

    mocker.patch.object(controller.service, "get_closest_flight")
    controller.service.get_closest_flight.return_value = mock_flight
    mocker.patch.object(controller.service, "get_score")
    controller.service.get_score.return_value = "mock_score"
    mocker.patch.object(controller.service, "update_player_score")

    mocker.patch.object(controller.validator, "validate_position")
    controller.validator.validate_position.return_value = True
    mocker.patch.object(controller.validator, "validate_airport_names")
    controller.validator.validate_airport_names.return_value = False
    mocker.patch.object(controller.validator, "validate_player_id")
    controller.validator.validate_player_id.return_value = True

    response = controller.handle_turn(
        test_longitude, test_latitude, test_origin, test_destination, test_player_id
    )

    assert response == '{"response": "Invalid airport names", "status": 400}'
    controller.service.get_closest_flight.assert_not_called()


def test_handle_turn_invalid_player_id(mocker):
    """test the response and function calls for the handle_turn controller function when the request is unsuccessful"""
    test_longitude = "10.000"
    test_latitude = "5.0000"
    test_origin = "test_origin"
    test_destination = "test_destination"
    test_player_id = "test_player_id"
    mock_flight = Flight()

    mocker.patch.object(controller.service, "get_closest_flight")
    controller.service.get_closest_flight.return_value = mock_flight
    mocker.patch.object(controller.service, "get_score")
    controller.service.get_score.return_value = "mock_score"
    mocker.patch.object(controller.service, "update_player_score")

    mocker.patch.object(controller.validator, "validate_position")
    controller.validator.validate_position.return_value = True
    mocker.patch.object(controller.validator, "validate_airport_names")
    controller.validator.validate_airport_names.return_value = True
    mocker.patch.object(controller.validator, "validate_player_id")
    controller.validator.validate_player_id.return_value = False

    response = controller.handle_turn(
        test_longitude, test_latitude, test_origin, test_destination, test_player_id
    )

    assert response == '{"response": "Invalid player ID", "status": 400}'
    controller.service.get_closest_flight.assert_not_called()
