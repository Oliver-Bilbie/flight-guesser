import os
import json
import traceback
from dataclasses import asdict
from helpers.data_types import GameRules
from helpers.make_guess import make_guess
from helpers.utils import HandledException, read_position
from multiplayer_helpers.player_type import Player
from multiplayer_helpers.lobby_type import Lobby
import boto3


WEBSOCKET_ENDPOINT = os.getenv("WEBSOCKET_ENDPOINT").replace("wss", "https", 1)
API_CLIENT = boto3.client(
    "apigatewaymanagementapi",
    endpoint_url=WEBSOCKET_ENDPOINT,
)


def lambda_handler(event, context):
    connection_id = event["requestContext"]["connectionId"]
    route_key = event["requestContext"]["routeKey"]
    input_body = json.loads(event.get("body"))

    print(f"Body: {input_body}")

    if route_key == "$connect":
        return connect_client(connection_id, input_body)

    if route_key == "$disconnect":
        return disconnect_client(connection_id)

    if route_key == "handle_guess":
        return handle_guess(connection_id, input_body)

    return {"statusCode": 400, "body": "Unsupported route"}


def connect_client(connection_id, input_body):
    is_new_lobby = input_body.get("is_new_lobby")
    player_name = sanitize_player_name(input_body.get("player_name"))

    if is_new_lobby:
        rules_input = input_body.get("rules")
        rules = GameRules(
            use_origin=rules_input.get("use_origin"),
            use_destination=rules_input.get("use_destination"),
        )
        lobby = Lobby.create(rules)

    else:
        lobby_id = input_body.get("lobby_id")
        lobby = Lobby.read(lobby_id)

    player = Player.from_db(player_name, lobby.id, connection_id)
    if player is None:
        player = Player.create(player_name, lobby.id, connection_id)

    # Push lobby players data to the connecting client
    player_data = list(map(lambda p: p.to_dict(), lobby.get_players()))

    API_CLIENT.post_to_connection(
        ConnectionId=connection_id,
        Data=json.dumps(player_data),
    )

    return {"statusCode": 200}


def disconnect_client(connection_id):
    # Connection is managed by API Gateway, so there is nothing to do here
    return {"statusCode": 200}


def handle_guess(connection_id, input_body):
    try:
        lobby_id = input_body.get("lobby_id")
        player_name = input_body.get("player_name")

        lobby = Lobby.read(lobby_id)
        if lobby is None:
            raise HandledException("Lobby does not exist", 404)

        player = Player.from_db(player_name, lobby_id, connection_id)
        if player is None:
            raise HandledException("Player does not exist", 404)

        player_position = read_position(
            input_body.get("player"),
            "player",
            allow_missing=False,
        )

        origin_guess_pos = None
        if lobby.rules.use_origin:
            origin_guess_pos = read_position(
                input_body.get("origin"),
                "origin airport",
                allow_missing=False,
            )

        destination_guess_pos = None
        if lobby.rules.use_destination:
            destination_guess_pos = read_position(
                input_body.get("destination"),
                "destination airport",
                allow_missing=False,
            )

        guess_result = make_guess(
            player_position,
            origin_guess_pos,
            destination_guess_pos,
            lobby.rules,
        )

        player.handle_guess(guess_result)

        # Push lobby players data to the connecting client
        lobby_players = lobby.get_players()
        lobby_data = json.dumps(list(map(lambda p: p.to_dict(), lobby_players)))

        for lobby_player in lobby_players:
            try:
                API_CLIENT.post_to_connection(
                    ConnectionId=lobby_player.connection_id,
                    Data=lobby_data,
                )
            except Exception as e:
                print(
                    f"[WARN] Failed to send to connection {lobby_player.connection_id}: {e}"
                )

        return {
            "statusCode": 200,
            "body": json.dumps(asdict(guess_result)),
        }

    except HandledException as exc:
        return exc.to_response()

    except Exception as exc:
        print(f"[ERROR] {str(exc)}")
        print(traceback.format_exc())
        return {
            "statusCode": 500,
            "body": "The server was unable to process your request",
        }


def sanitize_player_name(name: str) -> str:
    name = name.strip()

    if not 1 <= len(name) <= 20:
        raise HandledException("Name must be 1–20 characters", 400)

    if not all(c.isalnum() or c in " '" for c in name):
        raise HandledException("Name may not include special characters", 400)

    return name
