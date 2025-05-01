import json
from typing import Any, Union
from helpers.data_types import Position, GameRules


class HandledException(Exception):
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

    def to_response(self):
        return {
            "statusCode": self.status_code,
            "body": json.dumps({"message": self.message}),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": False,
            },
            "isBase64Encoded": False,
        }


def read_position(item: dict, item_name: str, allow_missing: bool = False) -> Position:
    try:
        return Position(lon=item.get("lon"), lat=item.get("lat"))
    except Exception as exc:
        if allow_missing:
            return None
        raise HandledException(f"The provided {item_name} position is invalid") from exc


def read_rules(rules_input: dict) -> GameRules:
    try:
        return GameRules(
            use_origin=rules_input.get("useOrigin"),
            use_destination=rules_input.get("useDestination"),
        )
    except Exception as exc:
        raise HandledException("The provided rules are invalid") from exc


def get_nested(data: Union[dict, list], *path) -> Any:
    """Safely get a nested value from a dict or list, or return None if any key/index is missing."""
    for key in path:
        try:
            data = data[key]
        except:
            return None

    return data
