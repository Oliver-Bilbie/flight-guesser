import json
from urllib.request import Request, urlopen
from urllib.parse import urlencode

HEADERS = {
    "cache-control": "max-age=0",
    "user-agent": "Mozilla/5.0 (Windows NT 6.1)",
}


def get_all_flights(position, serach_area_deg=0.2):
    bounds = ",".join(
        [
            str(position.lat + serach_area_deg),
            str(position.lat - serach_area_deg),
            str(position.lon + serach_area_deg),
            str(position.lon - serach_area_deg),
        ]
    )

    params = {
        "faa": 1,
        "satellite": 1,
        "mlat": 1,
        "flarm": 1,
        "adsb": 1,
        "gnd": 1,
        "air": 1,
        "vehicles": 1,
        "estimated": 1,
        "maxage": 14400,
        "gliders": 1,
        "stats": 1,
        "limit": 5000,
        "bounds": bounds,
    }

    url = f"https://data-cloud.flightradar24.com/zones/fcgi/feed.js?{urlencode(params)}"
    all_flights = make_request(url)
    return all_flights


def get_flight_details(flight_id):
    url = f"https://data-live.flightradar24.com/clickhandler/?flight={flight_id}"
    flight_details = make_request(url)
    return flight_details


def get_all_airports():
    url = "https://www.flightradar24.com/_json/airports.php"
    all_airports = make_request(url)
    return all_airports


def make_request(url):
    req = Request(url, headers=HEADERS)

    with urlopen(req) as fr_response:
        response = json.loads(fr_response.read().decode())

    return response
