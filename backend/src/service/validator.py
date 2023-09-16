"""Validation functions for user inputs"""

import re
from src.service.error_handling import ValidationException


def validate_position(longitude, latitude):
    """
    Raises a ValidationException if the position is invalid

    Args:
        longitude [float]: longitude to search from
        latitude [float]: latitude to search from
    """

    try:
        # Check that the values may be converted to floats
        longitude_float = float(longitude)
        latitude_float = float(latitude)

        # Check that the values are within the physical limits
        if abs(longitude_float) > 180 or abs(latitude_float) > 90:
            raise ValidationException("Invalid position")

    except ValueError as exc:
        raise ValidationException("Invalid position") from exc


def validate_airport_names(origin, destination):
    """
    Raises a ValidationException if the airport names are invalid

    Args:
        origin [string]: origin airport guess
        destination [string]: destination airport guess
    """

    for airport_name in [origin, destination]:
        # Check that the length is sensible
        if len(airport_name) > 50:
            raise ValidationException("Invalid airport names")

        # Check for special characters
        regex = re.compile("[@_!#$%^&*()<>?/|}{~:=]")
        if regex.search(airport_name) is not None:
            raise ValidationException("Invalid airport names")


def validate_player_id(player_id):
    """
    Raises a ValidationException if the player ID is invalid

    Args:
        player_id [string]: ID of the player
    """

    # Check that the length is correct
    if len(player_id) != 36:
        raise ValidationException("Invalid player ID")

    # Check for special characters
    regex = re.compile("[@_!#$%^&*()<>?/|}{~:=]")
    if regex.search(player_id) is not None:
        raise ValidationException("Invalid player ID")


def validate_player_name(name):
    """
    Raises a ValidationException if the player name is invalid

    Args:
        name [string]: Name of the player
    """

    # Check that the length is valid
    if len(name) > 16:
        raise ValidationException("Invalid name")

    # Check for special characters
    regex = re.compile("[@_!#$%^&*()<>?/|}{~:=]")
    if regex.search(name) is not None:
        raise ValidationException("Invalid name")


def validate_score(score):
    """
    Raises a ValidationException if the score is invalid

    Args:
        score [string]: Score of the player
    """

    try:
        # Check that the value may be converted to an integer
        score_int = int(score)

        # Check that the value is not less than zero
        if score_int < 0:
            raise ValidationException("Invalid score")

    except ValueError as exc:
        raise ValidationException("Invalid score") from exc


def validate_lobby_id(lobby_id):
    """
    Raises a ValidationException if the lobby ID is invalid

    Args:
        lobby_id [string]: ID of the lobby to join
    """

    # Check that the length is valid
    if len(lobby_id) != 4:
        raise ValidationException("Invalid lobby ID")

    # Check for forbidden characters
    regex = re.compile("[@_!#$%^&*()<>?/|}{~:=a-z0-9]")
    if regex.search(lobby_id) is not None:
        raise ValidationException("Invalid lobby ID")
