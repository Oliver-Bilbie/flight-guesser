"""Unit tests for the API functions"""

import json
from unittest import mock
from src.service import api


def test_get_airports(mocker):
    """
    Test the response and function calls for the get_airports api function
    """
    test_event = {}

    mocker.patch.object(api.controller, "get_airports")
    api.controller.get_airports.return_value = "expected_response"

    actual_response = api.get_airports(test_event, None)

    assert actual_response == "expected_response"
    api.controller.get_airports.assert_called_once()


def test_handle_turn(mocker):
    """
    Test the response and function calls for the handle_turn api function
    """
    test_event = {
        "body": json.dumps(
            {
                "longitude": "1",
                "latitude": "2",
                "origin": "test_origin",
                "destination": "test_destination",
                "player_id": "player_id",
            }
        )
    }

    mocker.patch.object(api.controller, "handle_turn")
    api.controller.handle_turn.return_value = "expected_response"

    actual_response = api.handle_turn(test_event, None)

    assert actual_response == "expected_response"
    api.controller.handle_turn.assert_called_once_with(
        "1", "2", "test_origin", "test_destination", "player_id"
    )


def test_create_lobby(mocker):
    """
    Test the response and function calls for the create_lobby api function
    """
    test_event = {
        "body": json.dumps(
            {
                "name": "test_name",
                "score": "test_score",
                "guessed_flights": "test_guessed_flights",
                "rules": "test_rules",
            }
        )
    }

    mocker.patch.object(api.controller, "create_lobby")
    api.controller.create_lobby.return_value = "expected_response"

    actual_response = api.create_lobby(test_event, None)

    assert actual_response == "expected_response"
    api.controller.create_lobby.assert_called_once_with(
        "test_name", "test_score", "test_guessed_flights", "test_rules"
    )


def test_join_lobby(mocker):
    """
    Test the response and function calls for the join_lobby api function
    """
    test_event = {
        "body": json.dumps(
            {
                "lobby_id": "test_lobby_id",
                "name": "test_name",
                "score": "test_score",
                "guessed_flights": "test_guessed_flights",
            }
        )
    }

    mocker.patch.object(api.controller, "join_lobby")
    api.controller.join_lobby.return_value = "expected_response"

    actual_response = api.join_lobby(test_event, None)

    assert actual_response == "expected_response"
    api.controller.join_lobby.assert_called_once_with(
        "test_lobby_id", "test_name", "test_score", "test_guessed_flights"
    )


def test_get_lobby_scores(mocker):
    """
    Test the response and function calls for the get_lobby_scores
    api function
    """
    test_event = {
        "pathParameters": {"lobby_id": "test_lobby_id"},
    }

    mocker.patch.object(api.controller, "get_lobby_scores")
    api.controller.get_lobby_scores.return_value = "expected_response"

    actual_response = api.get_lobby_scores(test_event, None)

    assert actual_response == "expected_response"
    api.controller.get_lobby_scores.assert_called_once_with("test_lobby_id")


def test_delete_lobby(mocker):
    """
    Test the response and function calls for the delete_lobby api function
    """
    mocker.patch.object(api.service, "delete_old_data")

    api.delete_lobby(None, None)

    api.service.delete_old_data.assert_called_once()
