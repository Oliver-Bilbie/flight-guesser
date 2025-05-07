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


MULTIPLAYER_ENDPOINT = os.getenv("MULTIPLAYER_ENDPOINT").replace("wss", "https", 1)
API_CLIENT = boto3.client(
    "apigatewaymanagementapi",
    endpoint_url=MULTIPLAYER_ENDPOINT,
)


def lambda_handler(event, context):
    connection_id = event["requestContext"]["connectionId"]
    route_key = event["requestContext"]["routeKey"]

    if route_key == "$connect":
        return {"statusCode": 200}

    if route_key == "$disconnect":
        return {"statusCode": 200}

    if route_key == "ping":
        return {"statusCode": 200}

    input_body = json.loads(event.get("body"))

    if route_key == "create_lobby":
        return create_lobby(connection_id, input_body)

    if route_key == "join_lobby":
        return join_lobby(connection_id, input_body)

    if route_key == "handle_guess":
        return handle_guess(connection_id, input_body)

    return {"statusCode": 400, "message": "Unsupported route"}


def create_lobby(connection_id, input_body):
    try:
        player_name = sanitize_player_name(input_body.get("player_name"))
        rules_input = input_body.get("rules")
        rules = GameRules(
            use_origin=rules_input.get("use_origin"),
            use_destination=rules_input.get("use_destination"),
        )

        lobby = Lobby.create(rules)
        player = Player.create(player_name, lobby.id, connection_id)

        player_data = list(map(lambda p: p.to_dict(), lobby.get_players()))

        post_to_connection(
            connection_id,
            {
                "event": "lobby_joined",
                "lobby": lobby.id,
                "rules": asdict(lobby.rules),
                "players": player_data,
                "player_name": player.name,
                "score": player.score,
            },
        )

    except HandledException as exc:
        post_to_connection(
            connection_id,
            exc.to_ws_response("lobby_error"),
        )

    except Exception as exc:
        print(f"[ERROR] {str(exc)}")
        print(traceback.format_exc())
        post_to_connection(
            connection_id,
            {
                "event": "error",
                "message": "The server was unable to process your request",
            },
        )

    return {"statusCode": 200}


def join_lobby(connection_id, input_body):
    try:
        player_name = sanitize_player_name(input_body.get("player_name"))
        lobby_id = input_body.get("lobby_id")

        lobby = Lobby.read(lobby_id)

        player = Player.from_db(player_name, lobby.id, connection_id)
        if player is None:
            player = Player.create(player_name, lobby.id, connection_id)

        player_data = list(map(lambda p: p.to_dict(), lobby.get_players()))

        post_to_connection(
            connection_id,
            {
                "event": "lobby_joined",
                "lobby": lobby.id,
                "rules": asdict(lobby.rules),
                "players": player_data,
                "player_name": player.name,
                "score": player.score,
            },
        )

    except HandledException as exc:
        post_to_connection(
            connection_id,
            exc.to_ws_response("lobby_error"),
        )

    except Exception as exc:
        print(f"[ERROR] {str(exc)}")
        print(traceback.format_exc())
        post_to_connection(
            connection_id,
            {
                "event": "error",
                "message": "The server was unable to process your request",
            },
        )

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

        already_guessed = player.already_guessed(guess_result.flight.id)
        points_available = (
            lobby.rules.use_origin and guess_result.flight.origin is not None
        ) or (
            lobby.rules.use_destination and guess_result.flight.destination is not None
        )

        status = "Success"
        if already_guessed:
            status = "AlreadyGuessed"
        elif not points_available:
            status = "PointsUnavailable"

        player.handle_guess(guess_result)

        # Push lobby players data to the connecting client
        lobby_players = lobby.get_players()
        lobby_data = {
            "event": "lobby_update",
            "lobby_data": list(map(lambda p: p.to_dict(), lobby_players)),
        }

        for lobby_player in lobby_players:
            try:
                post_to_connection(lobby_player.connection_id, lobby_data)
            except Exception as e:
                print(
                    f"[WARNING] Failed to send to connection {lobby_player.connection_id}: {e}"
                )

        post_to_connection(
            connection_id,
            {
                "event": "flight_details",
                "status": status,
                "score": player.score,
                **asdict(guess_result),
            },
        )

    except HandledException as exc:
        post_to_connection(
            connection_id,
            exc.to_ws_response("flight_error"),
        )

    except Exception as exc:
        print(f"[ERROR] {str(exc)}")
        print(traceback.format_exc())
        post_to_connection(
            connection_id,
            {
                "event": "error",
                "message": "The server was unable to process your request",
            },
        )

    return {"statusCode": 200}


def sanitize_player_name(name: str) -> str:
    name = name.strip()

    if not 1 <= len(name) <= 20:
        raise HandledException("Name must be 1–20 characters", 400)

    if not all(c.isalnum() or c in " '" for c in name):
        raise HandledException("Name may not include special characters", 400)

    return name


def post_to_connection(connection_id, body):
    API_CLIENT.post_to_connection(
        ConnectionId=connection_id,
        Data=json.dumps(body).encode("utf-8"),
    )
