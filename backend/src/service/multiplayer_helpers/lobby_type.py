import random
import string
from datetime import datetime, timezone
from dataclasses import asdict
from helpers.data_types import GameRules
from multiplayer_helpers.db import LOBBY_TABLE, PLAYER_TABLE
from multiplayer_helpers.player_type import Player
from boto3.dynamodb.conditions import Key


class Lobby:
    def __init__(self, lobby_id: str, rules: GameRules):
        self._id = lobby_id
        self._rules = rules

    @property
    def id(self):
        return self._id

    @property
    def rules(self):
        return self._rules

    @classmethod
    def create(cls, rules: GameRules):
        is_unique = False
        while not is_unique:
            # Generate a random four-letter string
            lobby_id = "".join(random.choice(string.ascii_uppercase) for i in range(4))
            # Confirm that this lobby ID is not already in use
            existing_lobby = Lobby.read(lobby_id)
            if existing_lobby is None:
                is_unique = True

        LOBBY_TABLE.put_item(
            Item={
                "lobby_id": lobby_id,
                "last_interaction": datetime.now(timezone.utc).isoformat(),
                **asdict(rules),
            }
        )
        lobby = cls(lobby_id, rules)

        return lobby

    @classmethod
    def read(cls, lobby_id: str):
        response = LOBBY_TABLE.get_item(Key={"lobby_id": lobby_id})
        lobby_record = response.get("Item")

        if lobby_record is None:
            return None

        use_origin = lobby_record.get("use_origin")
        use_destination = lobby_record.get("use_destination")

        rules = GameRules(
            use_origin=use_origin,
            use_destination=use_destination,
        )

        lobby = cls(lobby_id, rules)

        return lobby

    def delete(self):
        LOBBY_TABLE.delete_item(Key={"lobby_id": self.id})
        return None

    def get_players(self):
        items = PLAYER_TABLE.query(
            KeyConditionExpression=Key("lobby_id").eq(self.id),
            IndexName="LobbyIndex",
        ).get("Items")

        players = list(map(Player.from_dict, items))

        return players
