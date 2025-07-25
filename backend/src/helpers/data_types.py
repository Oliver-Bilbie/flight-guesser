from typing import Optional
from dataclasses import dataclass


@dataclass
class Position:
    lat: float
    lon: float


@dataclass
class AirportGuess:
    position: Position
    enabled: bool


@dataclass
class AirportInfo:
    name: str
    city: Optional[str]
    iata: str
    icao: str
    position: Position


@dataclass
class Flight:
    id: str
    flight_number: str
    callsign: str
    airline: str
    aircraft_type: str
    aircraft_registration: str
    image_src: Optional[str]
    origin: AirportInfo
    destination: AirportInfo
    position: Position


@dataclass
class Points:
    origin: int
    destination: int
    total: int


@dataclass
class GuessResult:
    points: Points
    flight: Flight


@dataclass
class GameRules:
    use_origin: bool
    use_destination: bool
