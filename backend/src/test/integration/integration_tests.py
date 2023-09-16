"""Integration tests for the API endpoints"""

import json
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
    """
    Test the get_airports function when the flight-radar api call is successful
    """
    event = {}

    airports = [
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
    api.controller.service.fr_api.get_airports.return_value = airports

    actual_response = api.get_airports(event, None)

    assert actual_response == json.dumps(
        {
            "response": ["test_airport", "test_airport_2", "test_airport_3"],
            "status": 200,
        }
    )
    api.controller.service.fr_api.get_airports.assert_called_once()


def test_get_airports_failure(mocker):
    """
    Test the get_airports function when the flight-radar api call is unsuccessful
    """
    event = {}

    mocker.patch.object(api.controller.service.fr_api, "get_airports")
    api.controller.service.fr_api.get_airports.side_effect = Exception("test_error")

    actual_response = api.get_airports(event, None)

    assert actual_response == json.dumps(
        {"response": "The server was unable to process your request", "status": 500}
    )
    api.controller.service.fr_api.get_airports.assert_called_once()


def test_handle_turn_success_correct_guesses(mocker):
    """
    Test the handle_turn function when the flight-radar api call is successful
    and the origin and destination are guessed correctly
    """
    event = {
        "body": json.dumps(
            {
                "longitude": "8.541694",
                "latitude": "47.376888",
                "origin": "Lugano Airport",
                "destination": "Lahr Black Forest Airport",
                "player_id": "fa97a7f7-ddb6-4515-965e-ee1bcf28f25e",
            }
        )
    }

    mocker.patch.object(api.controller.service.fr_api, "get_airports")
    mocker.patch.object(api.controller.service.fr_api, "get_flights")
    api.controller.service.fr_api.get_flights.return_value = [flight_data]
    mocker.patch.object(api.controller.service.fr_api, "get_flight_details")
    api.controller.service.fr_api.get_flight_details.return_value = details
    mocker.patch.object(api.controller.service, "player_table")
    api.controller.service.player_table.get_item.return_value = {
        "Item": {"lobby_id": "ABCD", "guessed_flights": "123,456,789"}
    }
    mocker.patch.object(api.controller.service, "lobby_table")
    api.controller.service.lobby_table.get_item.return_value = {"Item": {"rules": "3"}}

    actual_response = api.handle_turn(event, None)

    assert actual_response == json.dumps(
        {
            "response": {
                "id": "2cbce32c",
                "origin": "Lugano Airport",
                "destination": "Lahr Black Forest Airport",
                "aircraft": "BE9L",
                "score": 200,
            },
            "status": 200,
        }
    )
    api.controller.service.fr_api.get_airports.assert_not_called()
    api.controller.service.fr_api.get_flights.assert_called_once_with(
        bounds="47.386888,47.366888,8.531694,8.551694"
    )
    api.controller.service.fr_api.get_flight_details.assert_called_once_with("2cbce32c")
    api.controller.service.player_table.update_item.assert_called_once_with(
        Key={"player_id": "fa97a7f7-ddb6-4515-965e-ee1bcf28f25e"},
        UpdateExpression="SET score = score + :val, guessed_flights = :fid",
        ExpressionAttributeValues={":val": 200, ":fid": "123,456,789,2cbce32c"},
    )


def test_handle_turn_success_perfect_origin_far_destination(mocker):
    """
    Test the handle_turn function when the flight-radar api call is successful
    and the destination guessed is close enough to score points
    """
    event = {
        "body": json.dumps(
            {
                "longitude": "8.541694",
                "latitude": "47.376888",
                "origin": "Lugano Airport",
                "destination": "Paris Beauvais-Tille Airport",
                "player_id": "fa97a7f7-ddb6-4515-965e-ee1bcf28f25e",
            }
        )
    }

    mocker.patch.object(api.controller.service.fr_api, "get_airports")
    api.controller.service.fr_api.get_airports.return_value = airport_data
    mocker.patch.object(api.controller.service.fr_api, "get_flights")
    api.controller.service.fr_api.get_flights.return_value = [flight_data]
    mocker.patch.object(api.controller.service.fr_api, "get_flight_details")
    api.controller.service.fr_api.get_flight_details.return_value = details
    mocker.patch.object(api.controller.service, "player_table")
    api.controller.service.player_table.get_item.return_value = {
        "Item": {"lobby_id": "ABCD", "guessed_flights": "123,456,789"}
    }
    mocker.patch.object(api.controller.service, "lobby_table")
    api.controller.service.lobby_table.get_item.return_value = {"Item": {"rules": "3"}}

    actual_response = api.handle_turn(event, None)

    assert actual_response == json.dumps(
        {
            "response": {
                "id": "2cbce32c",
                "origin": "Lugano Airport",
                "destination": "Lahr Black Forest Airport",
                "aircraft": "BE9L",
                "score": 117.0,
            },
            "status": 200,
        }
    )
    api.controller.service.fr_api.get_airports.assert_called_once()
    api.controller.service.fr_api.get_flights.assert_called_once_with(
        bounds="47.386888,47.366888,8.531694,8.551694"
    )
    api.controller.service.fr_api.get_flight_details.assert_called_once_with("2cbce32c")
    api.controller.service.player_table.update_item.assert_called_once_with(
        Key={"player_id": "fa97a7f7-ddb6-4515-965e-ee1bcf28f25e"},
        UpdateExpression="SET score = score + :val, guessed_flights = :fid",
        ExpressionAttributeValues={":val": 117, ":fid": "123,456,789,2cbce32c"},
    )


def test_handle_turn_success_close_guess(mocker):
    """
    Test the handle_turn function when the flight-radar api call is successful
    and the destination guessed is close enough to score points
    """
    event = {
        "body": json.dumps(
            {
                "longitude": "8.541694",
                "latitude": "47.376888",
                "origin": "Geneva International Airport",
                "destination": "Paris Beauvais-Tille Airport",
                "player_id": "fa97a7f7-ddb6-4515-965e-ee1bcf28f25e",
            }
        )
    }

    mocker.patch.object(api.controller.service.fr_api, "get_airports")
    api.controller.service.fr_api.get_airports.return_value = airport_data
    mocker.patch.object(api.controller.service.fr_api, "get_flights")
    api.controller.service.fr_api.get_flights.return_value = [flight_data]
    mocker.patch.object(api.controller.service.fr_api, "get_flight_details")
    api.controller.service.fr_api.get_flight_details.return_value = details
    mocker.patch.object(api.controller.service, "player_table")
    api.controller.service.player_table.get_item.return_value = {
        "Item": {"lobby_id": "ABCD", "guessed_flights": "123,456,789"}
    }
    mocker.patch.object(api.controller.service, "lobby_table")
    api.controller.service.lobby_table.get_item.return_value = {"Item": {"rules": "3"}}

    actual_response = api.handle_turn(event, None)

    assert actual_response == json.dumps(
        {
            "response": {
                "id": "2cbce32c",
                "origin": "Lugano Airport",
                "destination": "Lahr Black Forest Airport",
                "aircraft": "BE9L",
                "score": 58.0,
            },
            "status": 200,
        }
    )
    api.controller.service.fr_api.get_airports.assert_called_once()
    api.controller.service.fr_api.get_flights.assert_called_once_with(
        bounds="47.386888,47.366888,8.531694,8.551694"
    )
    api.controller.service.fr_api.get_flight_details.assert_called_once_with("2cbce32c")
    api.controller.service.player_table.update_item.assert_called_once_with(
        Key={"player_id": "fa97a7f7-ddb6-4515-965e-ee1bcf28f25e"},
        UpdateExpression="SET score = score + :val, guessed_flights = :fid",
        ExpressionAttributeValues={":val": 58, ":fid": "123,456,789,2cbce32c"},
    )


def test_handle_turn_success_far_guess(mocker):
    """
    Test the handle_turn function when the flight-radar api call is successful
    and the destination guessed is too far away to score points
    """
    event = {
        "body": json.dumps(
            {
                "longitude": "8.541694",
                "latitude": "47.376888",
                "origin": "Denver Rocky Mountain Metropolitan Airport",
                "destination": "Dallas Fort Worth International Airport",
                "player_id": "fa97a7f7-ddb6-4515-965e-ee1bcf28f25e",
            }
        )
    }

    mocker.patch.object(api.controller.service.fr_api, "get_airports")
    api.controller.service.fr_api.get_airports.return_value = airport_data
    mocker.patch.object(api.controller.service.fr_api, "get_flights")
    api.controller.service.fr_api.get_flights.return_value = [flight_data]
    mocker.patch.object(api.controller.service.fr_api, "get_flight_details")
    api.controller.service.fr_api.get_flight_details.return_value = details
    mocker.patch.object(api.controller.service, "player_table")
    api.controller.service.player_table.get_item.return_value = {
        "Item": {"lobby_id": "ABCD", "guessed_flights": "123,456,789"}
    }
    mocker.patch.object(api.controller.service, "lobby_table")
    api.controller.service.lobby_table.get_item.return_value = {"Item": {"rules": "3"}}

    actual_response = api.handle_turn(event, None)

    assert actual_response == json.dumps(
        {
            "response": {
                "id": "2cbce32c",
                "origin": "Lugano Airport",
                "destination": "Lahr Black Forest Airport",
                "aircraft": "BE9L",
                "score": 0.0,
            },
            "status": 200,
        }
    )
    api.controller.service.fr_api.get_airports.assert_called_once()
    api.controller.service.fr_api.get_flights.assert_called_once_with(
        bounds="47.386888,47.366888,8.531694,8.551694"
    )
    api.controller.service.fr_api.get_flight_details.assert_called_once_with("2cbce32c")
    api.controller.service.player_table.update_item.assert_called_once_with(
        Key={"player_id": "fa97a7f7-ddb6-4515-965e-ee1bcf28f25e"},
        UpdateExpression="SET score = score + :val, guessed_flights = :fid",
        ExpressionAttributeValues={":val": 0, ":fid": "123,456,789,2cbce32c"},
    )


def test_handle_turn_success_only_origin_guess(mocker):
    """
    Test the handle_turn function when the flight-radar api call is successful
    and the destination guessed is close enough to score points
    """
    event = {
        "body": json.dumps(
            {
                "longitude": "8.541694",
                "latitude": "47.376888",
                "origin": "Geneva International Airport",
                "destination": "",
                "player_id": "fa97a7f7-ddb6-4515-965e-ee1bcf28f25e",
            }
        )
    }

    mocker.patch.object(api.controller.service.fr_api, "get_airports")
    api.controller.service.fr_api.get_airports.return_value = airport_data
    mocker.patch.object(api.controller.service.fr_api, "get_flights")
    api.controller.service.fr_api.get_flights.return_value = [flight_data]
    mocker.patch.object(api.controller.service.fr_api, "get_flight_details")
    api.controller.service.fr_api.get_flight_details.return_value = details
    mocker.patch.object(api.controller.service, "player_table")
    api.controller.service.player_table.get_item.return_value = {
        "Item": {"lobby_id": "ABCD", "guessed_flights": "123,456,789"}
    }
    mocker.patch.object(api.controller.service, "lobby_table")
    api.controller.service.lobby_table.get_item.return_value = {"Item": {"rules": "3"}}

    actual_response = api.handle_turn(event, None)

    assert actual_response == json.dumps(
        {
            "response": {
                "id": "2cbce32c",
                "origin": "Lugano Airport",
                "destination": "Lahr Black Forest Airport",
                "aircraft": "BE9L",
                "score": 41.0,
            },
            "status": 200,
        }
    )
    api.controller.service.fr_api.get_airports.assert_called_once()
    api.controller.service.fr_api.get_flights.assert_called_once_with(
        bounds="47.386888,47.366888,8.531694,8.551694"
    )
    api.controller.service.fr_api.get_flight_details.assert_called_once_with("2cbce32c")
    api.controller.service.player_table.update_item.assert_called_once_with(
        Key={"player_id": "fa97a7f7-ddb6-4515-965e-ee1bcf28f25e"},
        UpdateExpression="SET score = score + :val, guessed_flights = :fid",
        ExpressionAttributeValues={":val": 41, ":fid": "123,456,789,2cbce32c"},
    )


def test_handle_turn_success_only_destination_guess(mocker):
    """
    Test the handle_turn function when the flight-radar api call is successful
    and the destination guessed is close enough to score points
    """
    event = {
        "body": json.dumps(
            {
                "longitude": "8.541694",
                "latitude": "47.376888",
                "origin": "",
                "destination": "Geneva International Airport",
                "player_id": "fa97a7f7-ddb6-4515-965e-ee1bcf28f25e",
            }
        )
    }

    mocker.patch.object(api.controller.service.fr_api, "get_airports")
    api.controller.service.fr_api.get_airports.return_value = airport_data
    mocker.patch.object(api.controller.service.fr_api, "get_flights")
    api.controller.service.fr_api.get_flights.return_value = [flight_data]
    mocker.patch.object(api.controller.service.fr_api, "get_flight_details")
    api.controller.service.fr_api.get_flight_details.return_value = details
    mocker.patch.object(api.controller.service, "player_table")
    api.controller.service.player_table.get_item.return_value = {
        "Item": {"lobby_id": "ABCD", "guessed_flights": "123,456,789"}
    }
    mocker.patch.object(api.controller.service, "lobby_table")
    api.controller.service.lobby_table.get_item.return_value = {"Item": {"rules": "3"}}

    actual_response = api.handle_turn(event, None)

    assert actual_response == json.dumps(
        {
            "response": {
                "id": "2cbce32c",
                "origin": "Lugano Airport",
                "destination": "Lahr Black Forest Airport",
                "aircraft": "BE9L",
                "score": 33.0,
            },
            "status": 200,
        }
    )
    api.controller.service.fr_api.get_airports.assert_called_once()
    api.controller.service.fr_api.get_flights.assert_called_once_with(
        bounds="47.386888,47.366888,8.531694,8.551694"
    )
    api.controller.service.fr_api.get_flight_details.assert_called_once_with("2cbce32c")
    api.controller.service.player_table.update_item.assert_called_once_with(
        Key={"player_id": "fa97a7f7-ddb6-4515-965e-ee1bcf28f25e"},
        UpdateExpression="SET score = score + :val, guessed_flights = :fid",
        ExpressionAttributeValues={":val": 33, ":fid": "123,456,789,2cbce32c"},
    )


def test_handle_turn_no_flights(mocker):
    """
    Test the handle_turn function when the flight-radar api call is successful
    but no flights are found nearby
    """
    event = {
        "body": json.dumps(
            {
                "longitude": "8.541694",
                "latitude": "47.376888",
                "origin": "Zurich Airport",
                "destination": "Dallas Fort Worth International Airport",
                "player_id": "fa97a7f7-ddb6-4515-965e-ee1bcf28f25e",
            }
        )
    }

    mocker.patch.object(api.controller.service.fr_api, "get_airports")
    mocker.patch.object(api.controller.service.fr_api, "get_flights")
    api.controller.service.fr_api.get_flights.return_value = []
    mocker.patch.object(api.controller.service.fr_api, "get_flight_details")
    mocker.patch.object(api.controller.service, "player_table")
    api.controller.service.player_table.get_item.return_value = {
        "Item": {"lobby_id": "ABCD", "guessed_flights": "123,456,789"}
    }
    mocker.patch.object(api.controller.service, "lobby_table")
    api.controller.service.lobby_table.get_item.return_value = {"Item": {"rules": "3"}}

    actual_response = api.handle_turn(event, None)

    assert actual_response == json.dumps(
        {"response": "No flights were found", "status": 400}
    )
    assert api.controller.service.fr_api.get_flights.call_count == 49
    api.controller.service.fr_api.get_airports.assert_not_called()
    api.controller.service.fr_api.get_flight_details.assert_not_called()
    api.controller.service.player_table.update_item.assert_not_called()


def test_handle_turn_failure(mocker):
    """
    Test the handle_turn function when the flight-radar api call is unsuccessful
    """
    event = {
        "body": json.dumps(
            {
                "longitude": "8.541694",
                "latitude": "47.376888",
                "origin": "Zurich Airport",
                "destination": "Dallas Fort Worth International Airport",
                "player_id": "fa97a7f7-ddb6-4515-965e-ee1bcf28f25e",
            }
        )
    }

    mocker.patch.object(api.controller.service.fr_api, "get_airports")
    mocker.patch.object(api.controller.service.fr_api, "get_flights")
    api.controller.service.fr_api.get_flights.side_effect = Exception("test_error")
    mocker.patch.object(api.controller.service.fr_api, "get_flight_details")
    mocker.patch.object(api.controller.service, "player_table")
    api.controller.service.player_table.get_item.return_value = {
        "Item": {"lobby_id": "ABCD", "guessed_flights": "123,456,789"}
    }
    mocker.patch.object(api.controller.service, "lobby_table")
    api.controller.service.lobby_table.get_item.return_value = {"Item": {"rules": "3"}}

    actual_response = api.handle_turn(event, None)

    assert actual_response == json.dumps(
        {"response": "The server was unable to process your request", "status": 500}
    )
    api.controller.service.fr_api.get_flights.assert_called_once_with(
        bounds="47.386888,47.366888,8.531694,8.551694"
    )
    api.controller.service.fr_api.get_airports.assert_not_called()
    api.controller.service.fr_api.get_flight_details.assert_not_called()
    api.controller.service.player_table.update_item.assert_not_called()


def test_handle_turn_bad_position(mocker):
    """
    Test the handle_turn function when the longitude is not a number
    """
    event = {
        "body": json.dumps(
            {
                "longitude": "Error",
                "latitude": "47.376888",
                "origin": "Zurich Airport",
                "destination": "Dallas Fort Worth International Airport",
                "player_id": "fa97a7f7-ddb6-4515-965e-ee1bcf28f25e",
            }
        )
    }

    mocker.patch.object(api.controller.service.fr_api, "get_airports")
    mocker.patch.object(api.controller.service.fr_api, "get_flights")
    mocker.patch.object(api.controller.service.fr_api, "get_flight_details")
    mocker.patch.object(api.controller.service, "player_table")
    api.controller.service.player_table.get_item.return_value = {
        "Item": {"lobby_id": "ABCD", "guessed_flights": "123,456,789"}
    }
    mocker.patch.object(api.controller.service, "lobby_table")
    api.controller.service.lobby_table.get_item.return_value = {"Item": {"rules": "3"}}

    actual_response = api.handle_turn(event, None)

    assert actual_response == json.dumps(
        {"response": "Invalid position", "status": 400}
    )
    api.controller.service.fr_api.get_flights.assert_not_called()
    api.controller.service.fr_api.get_airports.assert_not_called()
    api.controller.service.fr_api.get_flight_details.assert_not_called()
    api.controller.service.player_table.update_item.assert_not_called()


def test_handle_turn_bad_origin(mocker):
    """
    Test the handle_turn function when SQL injection is attempted in the
    origin field
    """
    event = {
        "body": json.dumps(
            {
                "longitude": "8.541694",
                "latitude": "47.376888",
                "origin": "SELECT * FROM PlayerData WHERE UserId = 105 OR 1=1;",
                "destination": "Dallas Fort Worth International Airport",
                "player_id": "fa97a7f7-ddb6-4515-965e-ee1bcf28f25e",
            }
        )
    }

    mocker.patch.object(api.controller.service.fr_api, "get_airports")
    mocker.patch.object(api.controller.service.fr_api, "get_flights")
    mocker.patch.object(api.controller.service.fr_api, "get_flight_details")
    mocker.patch.object(api.controller.service, "player_table")
    api.controller.service.player_table.get_item.return_value = {
        "Item": {"lobby_id": "ABCD", "guessed_flights": "123,456,789"}
    }
    mocker.patch.object(api.controller.service, "lobby_table")
    api.controller.service.lobby_table.get_item.return_value = {"Item": {"rules": "3"}}

    actual_response = api.handle_turn(event, None)

    assert actual_response == json.dumps(
        {"response": "Invalid airport names", "status": 400}
    )
    api.controller.service.fr_api.get_flights.assert_not_called()
    api.controller.service.fr_api.get_airports.assert_not_called()
    api.controller.service.fr_api.get_flight_details.assert_not_called()
    api.controller.service.player_table.update_item.assert_not_called()


def test_handle_turn_bad_player_id(mocker):
    """
    Test the handle_turn function when SQL injection is attempted in the
    player_id field
    """
    event = {
        "body": json.dumps(
            {
                "longitude": "8.541694",
                "latitude": "47.376888",
                "origin": "Zurich Airport",
                "destination": "Dallas Fort Worth International Airport",
                "player_id": "SELECT * FROM PlayerData WHERE UserId = 105 OR 1=1;",
            }
        )
    }

    mocker.patch.object(api.controller.service.fr_api, "get_airports")
    mocker.patch.object(api.controller.service.fr_api, "get_flights")
    mocker.patch.object(api.controller.service.fr_api, "get_flight_details")
    mocker.patch.object(api.controller.service, "player_table")
    api.controller.service.player_table.get_item.return_value = {
        "Item": {"lobby_id": "ABCD", "guessed_flights": "123,456,789"}
    }
    mocker.patch.object(api.controller.service, "lobby_table")
    api.controller.service.lobby_table.get_item.return_value = {"Item": {"rules": "3"}}

    actual_response = api.handle_turn(event, None)

    assert actual_response == json.dumps(
        {"response": "Invalid player ID", "status": 400}
    )
    api.controller.service.fr_api.get_flights.assert_not_called()
    api.controller.service.fr_api.get_airports.assert_not_called()
    api.controller.service.fr_api.get_flight_details.assert_not_called()
    api.controller.service.player_table.update_item.assert_not_called()
