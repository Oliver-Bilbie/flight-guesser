import math
from typing import Optional
from helpers.fr24_api import get_all_flights, get_flight_details
from helpers.data_types import (
    Position,
    GameRules,
    AirportInfo,
    Flight,
    Points,
    GuessResult,
)
from helpers.utils import get_nested, HandledException


def make_guess(
    player_pos: Position,
    origin_guess_pos: Position,
    destination_guess_pos: Position,
    rules: GameRules,
) -> GuessResult:
    flight = find_closest_flight(player_pos)

    if flight is None:
        raise HandledException(
            "No flights were found in your location", status_code=404
        )

    origin_points = 0
    if rules.use_origin and flight.origin is not None:
        origin_points = calculate_points(flight.origin.position, origin_guess_pos)

    destination_points = 0
    if rules.use_destination and flight.destination is not None:
        destination_points = calculate_points(
            flight.destination.position, destination_guess_pos
        )

    points = Points(
        origin=origin_points,
        destination=destination_points,
        total=origin_points + destination_points,
    )

    return GuessResult(points=points, flight=flight)


def read_flight_details(raw: dict) -> Flight:
    def parse_airport(data):
        if data:
            return AirportInfo(
                name=get_nested(data, "name"),
                city=get_nested(data, "position", "region", "city"),
                iata=get_nested(data, "code", "iata"),
                icao=get_nested(data, "code", "icao"),
                position=Position(
                    lat=get_nested(data, "position", "latitude"),
                    lon=get_nested(data, "position", "longitude"),
                ),
            )
        return None

    callsign = get_nested(raw, "identification", "callsign")
    flight_number = get_nested(raw, "identification", "number", "default")
    departure_time = get_nested(raw, "time", "real", "departure")
    unique_id = "-".join(str(x) for x in [callsign, flight_number, departure_time])

    return Flight(
        id=unique_id,
        flight_number=flight_number,
        callsign=callsign,
        airline=get_nested(raw, "airline", "name"),
        aircraft_type=get_nested(raw, "aircraft", "model", "text"),
        aircraft_registration=get_nested(raw, "aircraft", "registration"),
        image_src=get_nested(raw, "aircraft", "images", "medium", 0, "src"),
        origin=parse_airport(get_nested(raw, "airport", "origin")),
        destination=parse_airport(get_nested(raw, "airport", "destination")),
        position=Position(
            lat=get_nested(raw, "trail", 0, "lat"),
            lon=get_nested(raw, "trail", 0, "lng"),
        ),
    )


def find_closest_flight(position: Position) -> Optional[Flight]:
    all_flights = get_all_flights(position)

    max_dist_km = 120

    closest_flight_dist = float("inf")
    closest_flight_key = None
    closest_flight_data = None

    for key, data in all_flights.items():
        if not isinstance(data, list):
            continue  # Skip metadata keys

        dist = haversine(position, Position(lat=data[1], lon=data[2]))

        if dist < closest_flight_dist and dist <= max_dist_km:
            closest_flight_dist = dist
            closest_flight_key = key

    if closest_flight_key is None:
        return None

    closest_flight_data = read_flight_details(get_flight_details(closest_flight_key))

    position_missing = (
        closest_flight_data.position.lon is None
        or closest_flight_data.position.lat is None
    )
    if position_missing:
        closest_flight_data.position.lat = all_flights[closest_flight_key][1]
        closest_flight_data.position.lon = all_flights[closest_flight_key][2]

    return closest_flight_data


def haversine(pos_1: Position, pos_2: Position) -> float:
    """
    Calculate the distance in km between two longitude and latitude positions
    """
    earth_radius = 6378
    phi1 = math.radians(pos_1.lat)
    phi2 = math.radians(pos_2.lat)
    d_phi = math.radians(pos_2.lat - pos_1.lat)
    d_lambda = math.radians(pos_2.lon - pos_1.lon)

    a = (
        math.sin(d_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return earth_radius * c


def calculate_points(pos_1: Position, pos_2: Position) -> int:
    distance = haversine(pos_1, pos_2)
    points = math.floor(100 * math.exp(-distance / 250))
    return points
