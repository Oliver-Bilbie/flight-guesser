"""Validation functions for user inputs"""

import re


def validate_position(longitude, latitude):
    """
    Returns True if the position is valid, otherwise returns False.
    Args:
        longitude [float]: longitude to search from
        latitude [float]: latitude to search from
    Returns:
        [Boolean]: True if the position is valid, otherwise False
    """
    valid = True

    try:
        # Confirm that the values may be converted to floats
        longitude_float = float(longitude)
        latitude_float = float(latitude)

        # Validate that the values are within the physical limits
        if abs(longitude_float) > 180 or abs(latitude_float) > 90:
            valid = False

    except:
        valid = False

    return valid


def validate_airport_names(origin, destination):
    """
    Returns True if the airport names are valid, otherwise returns False.
    Args:
        origin [string]: origin airport guess
        destination [string]: destination airport guess
    Returns:
        [Boolean]: True if the names are valid, otherwise False
    """
    valid = True

    for airport_name in [origin, destination]:
        # Check that the length is sensible
        if len(airport_name) > 50:
            valid = False
        else:
            # Check for special characters
            regex = re.compile("[@_!#$%^&*()<>?/|}{~:=]")
            if regex.search(airport_name) != None:
                valid = False

    return valid


def validate_player_id(player_id):
    """
    Returns True if the Player ID is valid, otherwise returns False.
    Args:
        player_id [string]: ID of the player
    Returns:
        [Boolean]: True if the ID is valid, otherwise False
    """
    valid = True

    # Check that the length is correct
    if len(player_id) != 36:
        valid = False
    else:
        # Check for special characters
        regex = re.compile("[@_!#$%^&*()<>?/|}{~:=]")
        if regex.search(player_id) != None:
            valid = False

    return valid


def validate_player_name(name):
    """
    Returns True if the name is valid, otherwise returns False.
    Args:
        name [string]: Name of the player
    Returns:
        [Boolean]: True if the name is valid, otherwise False
    """
    valid = True

    # Check that the length is valid
    if len(name) > 16:
        valid = False
    else:
        # Check for special characters
        regex = re.compile("[@_!#$%^&*()<>?/|}{~:=]")
        if regex.search(name) != None:
            valid = False

    return valid


def validate_score(score):
    """
    Returns True if the score is valid, otherwise returns False.
    Args:
        score [string]: Score of the player
    Returns:
        [Boolean]: True if the score is valid, otherwise False
    """
    valid = True

    try:
        # Confirm that the value may be converted to a float
        score_float = float(score)

        # Validate that the value is not less than zero
        if score_float < 0:
            valid = False

    except:
        valid = False

    return valid


def validate_lobby_id(lobby_id):
    """
    Returns True if the Lobby ID is valid, otherwise returns False.
    Args:
        lobby_id [string]: ID of the lobby to join
    Returns:
        [Boolean]: True if the ID is valid, otherwise False
    """
    valid = True

    # Check that the length is valid
    if len(lobby_id) != 4:
        valid = False
    else:
        # Check for forbidden characters
        regex = re.compile("[@_!#$%^&*()<>?/|}{~:=a-z0-9]")
        if regex.search(lobby_id) != None:
            valid = False

    return valid
