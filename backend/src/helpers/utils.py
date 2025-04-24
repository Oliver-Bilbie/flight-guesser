from helpers.data_types import Position, GameRules


class HandledException(Exception):
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

    def to_response(self):
        return {"statusCode": self.status_code, "message": self.message}


def read_position(item: dict, item_name: str, allow_missing: bool = False) -> Position:
    try:
        return Position(lon=item.get("lon"), lat=item.get("lat"))
    except Exception as exc:
        if allow_missing:
            return None
        raise ValueError(
            f"Unable to read the position values of the {item_name}"
        ) from exc


def read_rules(rules_input: dict) -> GameRules:
    try:
        return GameRules(
            use_origin=rules_input.get("use_origin"),
            use_destination=rules_input.get("use_destination"),
        )
    except Exception as exc:
        raise ValueError("Unable to read the game rules") from exc
