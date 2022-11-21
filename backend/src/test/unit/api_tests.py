"""unit tests for the API functions"""

from unittest import mock
from src.service import api


def test_get_airports(mocker):
    """test the response and function calls for the get_airports api function"""
    test_event = {}

    mocker.patch.object(api.controller, "get_airports")
    api.controller.get_airports.return_value = "expected_response"

    actual_response = api.get_airports(test_event, None)

    assert actual_response == "expected_response"
    api.controller.get_airports.assert_called_once()


def test_handle_turn(mocker):
    """test the response and function calls for the handle_turn api function"""
    test_event = {
        "body": '{"longitude": "1", "latitude": "2", "origin": "test_origin", "destination": "test_destination", "player_id": "player_id"}'
    }

    mocker.patch.object(api.controller, "handle_turn")
    api.controller.handle_turn.return_value = "expected_response"

    actual_response = api.handle_turn(test_event, None)

    assert actual_response == "expected_response"
    api.controller.handle_turn.assert_called_once_with(
        "1", "2", "test_origin", "test_destination", "player_id"
    )
