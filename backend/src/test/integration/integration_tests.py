"""integration tests for the application"""

import pickle
from unittest import mock
from src.service import api
from FlightRadar24.flight import Flight


# Load example API responses from pickle files
with open("src/test/resources/example_airports.pkl", "rb") as file:
    airport_data = pickle.load(file)
with open("src/test/resources/example_flight.pkl", "rb") as file:
    flight_data = pickle.load(file)
with open("src/test/resources/example_details.pkl", "rb") as file:
    details = pickle.load(file)


def test_get_airports_success(mocker):
    """test the get_airports function when the flight-radar api call is successful"""
    test_event = {}

    test_airports = [
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

    mocker.patch.object(api.controller.service.fr_api, "get_airports")
    api.controller.service.fr_api.get_airports.return_value = test_airports

    actual_response = api.get_airports(test_event, None)

    assert (
        actual_response
        == '{"response": ["test_airport", "test_airport_2", "test_airport_3"], "status": 200}'
    )
    api.controller.service.fr_api.get_airports.assert_called_once()


def test_get_airports_failure(mocker):
    """test the get_airports function when the flight-radar api call is unsuccessful"""
    test_event = {}

    mocker.patch.object(api.controller.service.fr_api, "get_airports")
    api.controller.service.fr_api.get_airports.side_effect = Exception("test_error")

    actual_response = api.get_airports(test_event, None)

    assert actual_response == '{"response": "An error has occurred.", "status": 500}'
    api.controller.service.fr_api.get_airports.assert_called_once()


def test_handle_turn_success_correct_guesses(mocker):
    """test the handle_turn function when the flight-radar api call is successful and the destination is guessed correctly"""
    test_event = {
        "body": '{"longitude": "8.541694", "latitude": "47.376888", "origin": "Lugano Airport", "destination": "Lahr Black Forest Airport", "player_id": "ff3efc7a-a555-4119-9b24-f60ebae5de20"}'
    }

    mocker.patch.object(api.controller.service.fr_api, "get_airports")
    mocker.patch.object(api.controller.service.fr_api, "get_flights")
    api.controller.service.fr_api.get_flights.return_value = [flight_data]
    mocker.patch.object(api.controller.service.fr_api, "get_flight_details")
    api.controller.service.fr_api.get_flight_details.return_value = details
    mocker.patch.object(api.controller.service, "lobbyTable")

    actual_response = api.handle_turn(test_event, None)

    assert (
        actual_response
        == '{"response": {"id": "2cbce32c", "origin": "Lugano Airport", "destination": "Lahr Black Forest Airport", "aircraft": "BE9L", "score": 200}, "status": 200}'
    )
    api.controller.service.fr_api.get_airports.assert_not_called()
    api.controller.service.fr_api.get_flights.assert_called_once_with(
        bounds="47.386888,47.366888,8.531694,8.551694"
    )
    api.controller.service.fr_api.get_flight_details.assert_called_once_with("2cbce32c")
    api.controller.service.lobbyTable.update_item.assert_called_once_with(
        Key={"player_id": "ff3efc7a-a555-4119-9b24-f60ebae5de20"},
        UpdateExpression="SET score = score + :val",
        ExpressionAttributeValues={":val": 200},
    )


def test_handle_turn_success_perfect_origin_far_destination(mocker):
    """test the handle_turn function when the flight-radar api call is successful and the destination guessed is close enough to score points"""
    test_event = {
        "body": '{"longitude": "8.541694", "latitude": "47.376888", "origin": "Lugano Airport", "destination": "Paris Beauvais-Tille Airport", "player_id": "ff3efc7a-a555-4119-9b24-f60ebae5de20"}'
    }

    mocker.patch.object(api.controller.service.fr_api, "get_airports")
    api.controller.service.fr_api.get_airports.return_value = airport_data
    mocker.patch.object(api.controller.service.fr_api, "get_flights")
    api.controller.service.fr_api.get_flights.return_value = [flight_data]
    mocker.patch.object(api.controller.service.fr_api, "get_flight_details")
    api.controller.service.fr_api.get_flight_details.return_value = details
    mocker.patch.object(api.controller.service, "lobbyTable")

    actual_response = api.handle_turn(test_event, None)

    assert (
        actual_response
        == '{"response": {"id": "2cbce32c", "origin": "Lugano Airport", "destination": "Lahr Black Forest Airport", "aircraft": "BE9L", "score": 100}, "status": 200}'
    )
    api.controller.service.fr_api.get_airports.assert_called_once()
    api.controller.service.fr_api.get_flights.assert_called_once_with(
        bounds="47.386888,47.366888,8.531694,8.551694"
    )
    api.controller.service.fr_api.get_flight_details.assert_called_once_with("2cbce32c")
    api.controller.service.lobbyTable.update_item.assert_called_once_with(
        Key={"player_id": "ff3efc7a-a555-4119-9b24-f60ebae5de20"},
        UpdateExpression="SET score = score + :val",
        ExpressionAttributeValues={":val": 100},
    )


def test_handle_turn_success_close_guess(mocker):
    """test the handle_turn function when the flight-radar api call is successful and the destination guessed is close enough to score points"""
    test_event = {
        "body": '{"longitude": "8.541694", "latitude": "47.376888", "origin": "Geneva International Airport", "destination": "Paris Beauvais-Tille Airport", "player_id": "ff3efc7a-a555-4119-9b24-f60ebae5de20"}'
    }

    mocker.patch.object(api.controller.service.fr_api, "get_airports")
    api.controller.service.fr_api.get_airports.return_value = airport_data
    mocker.patch.object(api.controller.service.fr_api, "get_flights")
    api.controller.service.fr_api.get_flights.return_value = [flight_data]
    mocker.patch.object(api.controller.service.fr_api, "get_flight_details")
    api.controller.service.fr_api.get_flight_details.return_value = details
    mocker.patch.object(api.controller.service, "lobbyTable")

    actual_response = api.handle_turn(test_event, None)

    assert (
        actual_response
        == '{"response": {"id": "2cbce32c", "origin": "Lugano Airport", "destination": "Lahr Black Forest Airport", "aircraft": "BE9L", "score": 11.0}, "status": 200}'
    )
    api.controller.service.fr_api.get_airports.assert_called_once()
    api.controller.service.fr_api.get_flights.assert_called_once_with(
        bounds="47.386888,47.366888,8.531694,8.551694"
    )
    api.controller.service.fr_api.get_flight_details.assert_called_once_with("2cbce32c")
    api.controller.service.lobbyTable.update_item.assert_called_once_with(
        Key={"player_id": "ff3efc7a-a555-4119-9b24-f60ebae5de20"},
        UpdateExpression="SET score = score + :val",
        ExpressionAttributeValues={":val": 11},
    )


def test_handle_turn_success_far_guess(mocker):
    """test the handle_turn function when the flight-radar api call is successful and the destination guessed is too far away to score points"""
    test_event = {
        "body": '{"longitude": "8.541694", "latitude": "47.376888", "origin": "Denver Rocky Mountain Metropolitan Airport", "destination": "Dallas Fort Worth International Airport", "player_id": "ff3efc7a-a555-4119-9b24-f60ebae5de20"}'
    }

    mocker.patch.object(api.controller.service.fr_api, "get_airports")
    api.controller.service.fr_api.get_airports.return_value = airport_data
    mocker.patch.object(api.controller.service.fr_api, "get_flights")
    api.controller.service.fr_api.get_flights.return_value = [flight_data]
    mocker.patch.object(api.controller.service.fr_api, "get_flight_details")
    api.controller.service.fr_api.get_flight_details.return_value = details
    mocker.patch.object(api.controller.service, "lobbyTable")

    actual_response = api.handle_turn(test_event, None)

    assert (
        actual_response
        == '{"response": {"id": "2cbce32c", "origin": "Lugano Airport", "destination": "Lahr Black Forest Airport", "aircraft": "BE9L", "score": 0}, "status": 200}'
    )
    api.controller.service.fr_api.get_airports.assert_called_once()
    api.controller.service.fr_api.get_flights.assert_called_once_with(
        bounds="47.386888,47.366888,8.531694,8.551694"
    )
    api.controller.service.fr_api.get_flight_details.assert_called_once_with("2cbce32c")
    api.controller.service.lobbyTable.update_item.assert_called_once_with(
        Key={"player_id": "ff3efc7a-a555-4119-9b24-f60ebae5de20"},
        UpdateExpression="SET score = score + :val",
        ExpressionAttributeValues={":val": 0},
    )


def test_handle_turn_success_only_origin_guess(mocker):
    """test the handle_turn function when the flight-radar api call is successful and the destination guessed is close enough to score points"""
    test_event = {
        "body": '{"longitude": "8.541694", "latitude": "47.376888", "origin": "Geneva International Airport", "destination": "", "player_id": "ff3efc7a-a555-4119-9b24-f60ebae5de20"}'
    }

    mocker.patch.object(api.controller.service.fr_api, "get_airports")
    api.controller.service.fr_api.get_airports.return_value = airport_data
    mocker.patch.object(api.controller.service.fr_api, "get_flights")
    api.controller.service.fr_api.get_flights.return_value = [flight_data]
    mocker.patch.object(api.controller.service.fr_api, "get_flight_details")
    api.controller.service.fr_api.get_flight_details.return_value = details
    mocker.patch.object(api.controller.service, "lobbyTable")

    actual_response = api.handle_turn(test_event, None)

    assert (
        actual_response
        == '{"response": {"id": "2cbce32c", "origin": "Lugano Airport", "destination": "Lahr Black Forest Airport", "aircraft": "BE9L", "score": 11.0}, "status": 200}'
    )
    api.controller.service.fr_api.get_airports.assert_called_once()
    api.controller.service.fr_api.get_flights.assert_called_once_with(
        bounds="47.386888,47.366888,8.531694,8.551694"
    )
    api.controller.service.fr_api.get_flight_details.assert_called_once_with("2cbce32c")
    api.controller.service.lobbyTable.update_item.assert_called_once_with(
        Key={"player_id": "ff3efc7a-a555-4119-9b24-f60ebae5de20"},
        UpdateExpression="SET score = score + :val",
        ExpressionAttributeValues={":val": 11},
    )


def test_handle_turn_success_only_destination_guess(mocker):
    """test the handle_turn function when the flight-radar api call is successful and the destination guessed is close enough to score points"""
    test_event = {
        "body": '{"longitude": "8.541694", "latitude": "47.376888", "origin": "", "destination": "Geneva International Airport", "player_id": "ff3efc7a-a555-4119-9b24-f60ebae5de20"}'
    }

    mocker.patch.object(api.controller.service.fr_api, "get_airports")
    api.controller.service.fr_api.get_airports.return_value = airport_data
    mocker.patch.object(api.controller.service.fr_api, "get_flights")
    api.controller.service.fr_api.get_flights.return_value = [flight_data]
    mocker.patch.object(api.controller.service.fr_api, "get_flight_details")
    api.controller.service.fr_api.get_flight_details.return_value = details
    mocker.patch.object(api.controller.service, "lobbyTable")

    actual_response = api.handle_turn(test_event, None)

    assert (
        actual_response
        == '{"response": {"id": "2cbce32c", "origin": "Lugano Airport", "destination": "Lahr Black Forest Airport", "aircraft": "BE9L", "score": 17.0}, "status": 200}'
    )
    api.controller.service.fr_api.get_airports.assert_called_once()
    api.controller.service.fr_api.get_flights.assert_called_once_with(
        bounds="47.386888,47.366888,8.531694,8.551694"
    )
    api.controller.service.fr_api.get_flight_details.assert_called_once_with("2cbce32c")
    api.controller.service.lobbyTable.update_item.assert_called_once_with(
        Key={"player_id": "ff3efc7a-a555-4119-9b24-f60ebae5de20"},
        UpdateExpression="SET score = score + :val",
        ExpressionAttributeValues={":val": 17},
    )


def test_handle_turn_no_flights(mocker):
    """test the handle_turn function when the flight-radar api call is successful but no flights are found nearby"""
    test_event = {
        "body": '{"longitude": "8.541694", "latitude": "47.376888", "origin": "Zurich Airport", "destination": "Dallas Fort Worth International Airport", "player_id": "ff3efc7a-a555-4119-9b24-f60ebae5de20"}'
    }

    mocker.patch.object(api.controller.service.fr_api, "get_airports")
    mocker.patch.object(api.controller.service.fr_api, "get_flights")
    api.controller.service.fr_api.get_flights.return_value = []
    mocker.patch.object(api.controller.service.fr_api, "get_flight_details")
    mocker.patch.object(api.controller.service, "lobbyTable")

    actual_response = api.handle_turn(test_event, None)

    assert actual_response == '{"response": "No flights were found", "status": 400}'
    assert api.controller.service.fr_api.get_flights.call_count == 49
    api.controller.service.fr_api.get_airports.assert_not_called()
    api.controller.service.fr_api.get_flight_details.assert_not_called()
    api.controller.service.lobbyTable.update_item.assert_not_called()


def test_handle_turn_failure(mocker):
    """test the handle_turn function when the flight-radar api call is unsuccessful"""
    test_event = {
        "body": '{"longitude": "8.541694", "latitude": "47.376888", "origin": "Zurich Airport", "destination": "Dallas Fort Worth International Airport", "player_id": "ff3efc7a-a555-4119-9b24-f60ebae5de20"}'
    }

    mocker.patch.object(api.controller.service.fr_api, "get_airports")
    mocker.patch.object(api.controller.service.fr_api, "get_flights")
    api.controller.service.fr_api.get_flights.side_effect = Exception("test_error")
    mocker.patch.object(api.controller.service.fr_api, "get_flight_details")
    mocker.patch.object(api.controller.service, "lobbyTable")

    actual_response = api.handle_turn(test_event, None)

    assert actual_response == '{"response": "An error has occurred.", "status": 500}'
    api.controller.service.fr_api.get_flights.assert_called_once_with(
        bounds="47.386888,47.366888,8.531694,8.551694"
    )
    api.controller.service.fr_api.get_airports.assert_not_called()
    api.controller.service.fr_api.get_flight_details.assert_not_called()
    api.controller.service.lobbyTable.update_item.assert_not_called()
