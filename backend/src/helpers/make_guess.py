import math
from typing import Optional
from helpers.fr24_api import get_all_flights, get_flight_details
from helpers.data_types import Position, GameRules, AirportInfo, Flight, GuessResult
from helpers.utils import HandledException


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

    score = 0

    if rules.use_origin:
        score += calculate_score(flight.origin.position, origin_guess_pos)

    if rules.use_destination:
        score += calculate_score(flight.destination.position, destination_guess_pos)

    return GuessResult(score=score, flight=flight)


def read_flight_details(raw: dict) -> Flight:
    airport = raw["airport"]
    origin = airport["origin"]
    destination = airport["destination"]

    def parse_airport(data):
        return AirportInfo(
            name=data["name"],
            city=data["position"]["region"].get("city"),
            iata=data["code"]["iata"],
            icao=data["code"]["icao"],
            position=Position(
                lat=data["position"]["latitude"],
                lon=data["position"]["longitude"],
            ),
        )

    def pick_first_image(images):
        try:
            return images.get("medium")[0]["src"]
        except:
            return None

    return Flight(
        flight_number=raw["identification"]["number"]["default"],
        callsign=raw["identification"]["callsign"],
        airline=raw["airline"]["name"],
        aircraft_type=raw["aircraft"]["model"]["text"],
        aircraft_registration=raw["aircraft"]["registration"],
        image_src=pick_first_image(raw["aircraft"].get("images", {})),
        origin=parse_airport(origin),
        destination=parse_airport(destination),
        position=Position(lat=raw["trail"][0]["lat"], lon=raw["trail"][0]["lng"]),
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


def calculate_score(pos_1: Position, pos_2: Position) -> int:
    distance = haversine(pos_1, pos_2)
    score = math.floor(100 * math.exp(-distance / 250))
    return score
