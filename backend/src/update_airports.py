"""
Service for automatically updating the airport data periodically
"""

import os
import json
import boto3
from helpers.fr24_api import get_all_airports

BUCKET_NAME = os.getenv("BUCKET_NAME")
s3_client = boto3.client("s3")


def lambda_handler(event, context):
    data = get_all_airports().get("rows")
    validate_api_response(data)
    airports = format_airport_data(data)

    s3_client.put_object(
        Bucket=BUCKET_NAME,
        Key="airports.json",
        Body=json.dumps(airports),
        ContentType="application/json",
    )

    return {"statusCode": 200, "body": "Airports were updated successfully"}


def format_airport_data(data: list) -> list:
    return [
        {
            "name": airport["name"],
            "iata": airport["iata"],
            "position": {
                "lat": airport["lat"],
                "lon": airport["lon"],
            },
            "icao": airport["icao"],
            "country": airport["country"],
            "city": None,
        }
        for airport in data
    ]


def validate_api_response(data: list):
    if not isinstance(data, list):
        raise ValueError("API response is not a list.")

    if len(data) == 0:
        raise ValueError("Airport list is empty")

    required_keys = {"name", "iata", "icao", "lat", "lon", "country"}
    string_keys = {"name", "iata", "icao", "country"}
    numeric_keys = {"lat", "lon"}

    for i, airport in enumerate(data):
        if not isinstance(airport, dict):
            raise ValueError(f"Item at index {i} is not a dictionary.")

        # Check for missing keys
        missing_keys = required_keys - airport.keys()
        if missing_keys:
            raise ValueError(f"Item at index {i} is missing keys: {missing_keys}")

        # Check types for string keys
        for key in string_keys:
            if not isinstance(airport[key], str):
                raise ValueError(f"Item at index {i}: '{key}' is not a string.")

        # Check types for numeric keys (float or int)
        for key in numeric_keys:
            if not isinstance(airport[key], (int, float)):
                raise ValueError(f"Item at index {i}: '{key}' is not a number.")
