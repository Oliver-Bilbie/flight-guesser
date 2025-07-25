from datetime import datetime, timezone
from helpers.data_types import GuessResult
from multiplayer_helpers.db import PLAYER_TABLE


class Player:
    @classmethod
    def get_id(cls, name: str, lobby: str):
        return f"{name}@{lobby}"

    def __init__(
        self,
        name: str,
        lobby: str,
        connection_id: str,
    ):
        self._id = Player.get_id(name, lobby)
        self._lobby = lobby
        self._name = name
        self._connection_id = connection_id
        self.score = int(0)
        self.guessed_flights = []

    @property
    def id(self):
        return self._id

    @property
    def lobby(self):
        return self._lobby

    @property
    def name(self):
        return self._name

    @property
    def connection_id(self):
        return self._connection_id

    @classmethod
    def create(cls, name: str, lobby: str, connection_id: str):
        player = cls(name, lobby, connection_id)
        PLAYER_TABLE.put_item(
            Item={
                "player_id": player.id,
                "lobby_id": player.lobby,
                "player_name": player.name,
                "connection_id": player.connection_id,
                "score": player.score,
                "guessed_flights": player.guessed_flights,
                "last_interaction": datetime.now(timezone.utc).isoformat(),
            }
        )
        return player

    @classmethod
    def from_db(cls, name: str, lobby: str, connection_id: str):
        player_id = Player.get_id(name, lobby)
        response = PLAYER_TABLE.get_item(Key={"player_id": player_id})
        player_record = response.get("Item")

        if player_record is None:
            return None

        player = cls(name, lobby, connection_id)
        player.score = int(player_record.get("score"))
        player.guessed_flights = player_record.get("guessed_flights")

        # Update connection_id if it has changed
        if player_record.get("connection_id") != connection_id:
            PLAYER_TABLE.update_item(
                Key={"player_id": player_id},
                UpdateExpression="SET connection_id = :c",
                ExpressionAttributeValues={":c": connection_id},
            )

        return player

    @classmethod
    def from_dict(cls, player_data: dict):
        name = player_data.get("player_name")
        lobby = player_data.get("lobby_id")
        connection_id = player_data.get("connection_id")
        score = player_data.get("score")
        guessed_flights = player_data.get("guessed_flights")

        player = cls(name, lobby, connection_id)
        player.score = int(score)
        player.guessed_flights = guessed_flights

        return player

    def update(self):
        PLAYER_TABLE.update_item(
            Key={"player_id": self.id},
            UpdateExpression=(
                "SET score = :s, guessed_flights = :g, "
                "last_interaction = :t, connection_id = :c"
            ),
            ExpressionAttributeValues={
                ":s": self.score,
                ":g": self.guessed_flights,
                ":t": datetime.now(timezone.utc).isoformat(),
                ":c": self.connection_id,
            },
        )

    @classmethod
    def disconnect(cls, name: str, lobby: str):
        player_id = Player.get_id(name, lobby)
        PLAYER_TABLE.update_item(
            Key={"player_id": player_id},
            UpdateExpression="SET connection_id = :c",
            ExpressionAttributeValues={":c": ""},
        )

    def delete(self):
        PLAYER_TABLE.delete_item(Key={"player_id": self.id})
        return None

    def already_guessed(self, flight_id: str):
        return flight_id in self.guessed_flights

    def handle_guess(self, result: GuessResult):
        f_id = result.flight.id
        isValidId = f_id is not None and f_id != "Blocked-None-None"

        if isValidId and not self.already_guessed(result.flight.id):
            self.score += int(result.points.origin)
            self.score += int(result.points.destination)
            self.guessed_flights.append(result.flight.id)
            self.update()

    def to_dict(self):
        return {
            "player_name": self.name,
            "score": self.score,
            "guess_count": len(self.guessed_flights),
        }
