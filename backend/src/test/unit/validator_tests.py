"""unit tests for the validator functions"""

import pytest
from contextlib import nullcontext as does_not_raise
from src.service import validator


@pytest.mark.parametrize(
    "latitude,longitude,expectation",
    [
        # London
        (51.507, -0.1278, does_not_raise()),
        # Tokyo
        (35.689, 129.69, does_not_raise()),
        # North Pole
        (90.000, 0, does_not_raise()),
        # Antarctica
        (-90.000, 0, does_not_raise()),
        # Pacific
        (0, 180, does_not_raise()),
        # Invalid longitude (big)
        (0, 200, pytest.raises(validator.ValidationException)),
        # Invalid longitude (small)
        (0, -200, pytest.raises(validator.ValidationException)),
        # Invalid latitude (big)
        (100, 0, pytest.raises(validator.ValidationException)),
        # Invalid latitude (small)
        (-100, 0, pytest.raises(validator.ValidationException)),
        # Invalid longitude (not numeric)
        ("this should fail", 0, pytest.raises(validator.ValidationException)),
        # Invalid latitude (not numeric)
        (0, "this should fail", pytest.raises(validator.ValidationException)),
        # Invalid longitude and latitude (not numeric)
        (
            "this should fail",
            "and so should this",
            pytest.raises(validator.ValidationException),
        ),
    ],
)
def test_validate_position(latitude, longitude, expectation):
    """
    Test that the position validator does nothing with valid inputs and raises
    a ValidationException with invalid inputs.
    """
    with expectation:
        validator.validate_position(longitude, latitude)


@pytest.mark.parametrize(
    "origin,destination,expectation",
    [
        # Zurich to Berlin
        ("Zurich Airport", "Berlin Brandenburg Airport", does_not_raise()),
        # Invalid origin (too long)
        (
            "SELECT * FROM PlayerData WHERE UserId = 105 OR 1=1;",
            "Berlin Brandenburg Airport",
            pytest.raises(validator.ValidationException),
        ),
        # Invalid destination (too long)
        (
            "Zurich Airport",
            "SELECT * FROM PlayerData WHERE UserId = 105 OR 1=1;",
            pytest.raises(validator.ValidationException),
        ),
        # Invalid origin (special characters)
        (
            "@@@@@",
            "Berlin Brandenburg Airport",
            pytest.raises(validator.ValidationException),
        ),
        # Invalid destination (special characters)
        ("Zurich Airport", "???", pytest.raises(validator.ValidationException)),
        # Invalid origin and destination (special characters)
        (
            "<Zurich Airport>",
            "SELECT * FROM Users WHERE UserId = 105 OR 1=1;",
            pytest.raises(validator.ValidationException),
        ),
    ],
)
def test_validate_airport_names(origin, destination, expectation):
    """
    Test that the airport name validator does nothing with valid inputs and
    raises a ValidationException with invalid inputs.
    """
    with expectation:
        validator.validate_airport_names(origin, destination)


@pytest.mark.parametrize(
    "player_id,expectation",
    [
        # Valid player ID
        ("d86bc44d-6e8a-40cb-8784-1331685faaa2", does_not_raise()),
        # Invalid player ID (too long)
        (
            "d86bc44d-6e8a-40cb-8784-1331685faaa21",
            pytest.raises(validator.ValidationException),
        ),
        # Invalid player ID (special characters)
        (
            "SELECT * FROM Users WHERE UserId = 1",
            pytest.raises(validator.ValidationException),
        ),
    ],
)
def test_validate_player_id(player_id, expectation):
    """
    Test that the player ID validator does nothing with valid inputs and
    raises a ValidationException with invalid inputs.
    """
    with expectation:
        validator.validate_player_id(player_id)


@pytest.mark.parametrize(
    "name,expectation",
    [
        # Valid name
        ("Michael Scott", does_not_raise()),
        # Invalid name (too long)
        (
            "Michael Scott of Dunder Mifflin Paper Company",
            pytest.raises(validator.ValidationException),
        ),
        # Invalid name (special characters)
        ("Michael $cott", pytest.raises(validator.ValidationException)),
    ],
)
def test_validate_player_name(name, expectation):
    """
    Test that the player name validator does nothing with valid inputs and
    raises a ValidationException with invalid inputs.
    """
    with expectation:
        validator.validate_player_name(name)


@pytest.mark.parametrize(
    "score,expectation",
    [
        # Valid score
        ("100", does_not_raise()),
        # Invalid score (negative)
        ("-1", pytest.raises(validator.ValidationException)),
        # Invalid score (not numeric)
        ("not a number", pytest.raises(validator.ValidationException)),
    ],
)
def test_validate_score(score, expectation):
    """
    Test that the score validator does nothing with valid inputs and
    raises a ValidationException with invalid inputs.
    """
    with expectation:
        validator.validate_score(score)


@pytest.mark.parametrize(
    "lobby_id,expectation",
    [
        # Valid lobby ID
        ("ABCD", does_not_raise()),
        # Invalid lobby ID (too long)
        ("ABCDE", pytest.raises(validator.ValidationException)),
        # Invalid lobby ID (too short)
        ("ABC", pytest.raises(validator.ValidationException)),
        # Invalid lobby ID (special characters)
        ("$@!%", pytest.raises(validator.ValidationException)),
        # Invalid lobby ID (numeric characters)
        ("ABC1", pytest.raises(validator.ValidationException)),
        # Invalid lobby ID (lowercase characters)
        ("abcd", pytest.raises(validator.ValidationException)),
    ],
)
def test_validate_lobby_id(lobby_id, expectation):
    """
    Test that the lobby ID validator does nothing with valid inputs and
    raises a ValidationException with invalid inputs.
    """
    with expectation:
        validator.validate_lobby_id(lobby_id)
