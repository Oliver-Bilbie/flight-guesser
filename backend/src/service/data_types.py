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
class GuessResult:
    success: bool
    score: Optional[int]
    flight: Optional[Flight]
    message: Optional[str]


@dataclass
class GameRules:
    use_origin: bool
    use_destination: bool
