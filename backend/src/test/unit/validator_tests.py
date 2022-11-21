"""unit tests for the validator functions"""

from src.service import validator


def test_validate_position_london():
    latitude = "51.507"
    longitude = "-0.1278"
    assert validator.validate_position(longitude, latitude)


def test_validate_position_tokyo():
    latitude = "35.689"
    longitude = "139.69"
    assert validator.validate_position(longitude, latitude)


def test_validate_position_north_pole():
    latitude = "90.000"
    longitude = "0"
    assert validator.validate_position(longitude, latitude)


def test_validate_position_antarctica():
    latitude = "-90.000"
    longitude = "0"
    assert validator.validate_position(longitude, latitude)


def test_validate_position_pacific():
    latitude = "0"
    longitude = "180"
    assert validator.validate_position(longitude, latitude)


def test_validate_position_big_longitude():
    latitude = "0"
    longitude = "200"
    assert not validator.validate_position(longitude, latitude)


def test_validate_position_small_longitude():
    latitude = "0"
    longitude = "-200"
    assert not validator.validate_position(longitude, latitude)


def test_validate_position_big_latitude():
    latitude = "100"
    longitude = "0"
    assert not validator.validate_position(longitude, latitude)


def test_validate_position_small_latitude():
    latitude = "-100"
    longitude = "0"
    assert not validator.validate_position(longitude, latitude)


def test_validate_position_not_numeric_longitude():
    latitude = "0"
    longitude = "this should fail"
    assert not validator.validate_position(longitude, latitude)


def test_validate_position_not_numeric_latitude():
    latitude = "this should fail"
    longitude = "0"
    assert not validator.validate_position(longitude, latitude)


def test_validate_position_not_numeric_both():
    latitude = "this should fail"
    longitude = "and so should this"
    assert not validator.validate_position(longitude, latitude)


def test_validate_airport_names_zurich_to_berlin():
    origin = "Zurich Airport"
    destination = "Berlin Brandenburg Airport"
    assert validator.validate_airport_names(origin, destination)


def test_validate_airport_names_origin_too_long():
    origin = "SELECT * FROM PlayerData WHERE UserId = 105 OR 1=1;"
    destination = "Berlin Brandenburg Airport"
    assert not validator.validate_airport_names(origin, destination)


def test_validate_airport_names_origin_too_long():
    origin = "Zurich Airport"
    destination = "SELECT * FROM PlayerData WHERE UserId = 105 OR 1=1;"
    assert not validator.validate_airport_names(origin, destination)


def test_validate_airport_names_invalid_origin():
    origin = "@@@@@"
    destination = "Berlin Brandenburg Airport"
    assert not validator.validate_airport_names(origin, destination)


def test_validate_airport_names_invalid_destination():
    origin = "Zurich Airport"
    destination = "???"
    assert not validator.validate_airport_names(origin, destination)


def test_validate_airport_names_both_invalid():
    origin = "<Zurich Airport>"
    destination = "SELECT * FROM Users WHERE UserId = 105 OR 1=1;"
    assert not validator.validate_airport_names(origin, destination)


def test_validate_player_id_valid():
    player_id = "d86bc44d-6e8a-40cb-8784-1331685faaa2"
    assert validator.validate_player_id(player_id)


def test_validate_player_id_invalid_length():
    player_id = "d86bc44d-6e8a-40cb-8784-1331685faaa21"
    assert not validator.validate_player_id(player_id)


def test_validate_player_id_invalid_characters():
    player_id = "SELECT * FROM Users WHERE UserId = 1"
    assert not validator.validate_player_id(player_id)


def test_validate_player_name_valid():
    name = "Michael Scott"
    assert validator.validate_player_name(name)


def test_validate_player_name_too_long():
    name = "Michael Scott of Dunder Mifflin Paper Company"
    assert not validator.validate_player_name(name)


def test_validate_player_name_invalid_characters():
    name = "Michael $cott"
    assert not validator.validate_player_name(name)


def test_validate_score_valid():
    score = "100"
    assert validator.validate_score(score)


def test_validate_score_less_than_zero():
    score = "-1"
    assert not validator.validate_score(score)


def test_validate_score_not_numeric():
    score = "not a number"
    assert not validator.validate_score(score)


def test_validate_lobby_id_valid():
    lobby_id = "ABCD"
    assert validator.validate_lobby_id(lobby_id)


def test_validate_lobby_too_long():
    lobby_id = "ABCDE"
    assert not validator.validate_lobby_id(lobby_id)


def test_validate_lobby_too_short():
    lobby_id = "ABC"
    assert not validator.validate_lobby_id(lobby_id)


def test_validate_lobby_special_characters():
    lobby_id = "$@!%"
    assert not validator.validate_lobby_id(lobby_id)


def test_validate_lobby_numeric_characters():
    lobby_id = "ABC1"
    assert not validator.validate_lobby_id(lobby_id)


def test_validate_lobby_lowercase_characters():
    lobby_id = "abcd"
    assert not validator.validate_lobby_id(lobby_id)
