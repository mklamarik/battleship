from fastapi.testclient import TestClient

from core.coordinate import Coordinate
from core.settings import settings
from core.ships.ship import Ship
from core.types import CellState
from services.game_service import GameService


def test_given_create_game_when_invalid_board_size_then_validation_error_is_returned(
    client: TestClient,
):
    response = client.post(
        "/api/v1/games",
        json={
            "player_1": "Alice",
            "player_2": "Bob",
            "board_size": 9,
        },
    )

    assert response.status_code == 422

    response = client.post(
        "/api/v1/games",
        json={
            "player_1": "Alice",
            "player_2": "Bob",
            "board_size": 21,
        },
    )

    assert response.status_code == 422


def test_given_make_move_when_coordinate_out_of_bounds_then_value_error_is_returned(
    client: TestClient,
) -> None:
    _ = client.post(
        "/api/v1/games", json={"player_1": "Alice", "player_2": "Bob", "board_size": 10}
    )

    response = client.post("/api/v1/games/moves", json={"x": 0, "y": 10})
    assert response.status_code == 422

    response = client.post("/api/v1/games/moves", json={"x": -1, "y": -30})
    assert response.status_code == 422


def test_given_create_game_when_game_is_created_then_correct_player_and_status_are_set(
    client: TestClient,
):
    response = client.post(
        "/api/v1/games",
        json={
            "player_1": "Alice",
            "player_2": "Bob",
            "board_size": 10,
        },
    )

    assert response.status_code == 200

    data = response.json()
    assert data["current_player"] == "Alice"
    assert data["status"] == "in progress"

    response = client.get("/api/v1/games")

    assert response.status_code == 200

    data = response.json()
    assert data["current_player"] == "Alice"
    assert data["status"] == "in progress"


def test_given_games_api_when_players_take_turns_then_players_are_switched_correctly(
    client: TestClient, game_service: GameService
):
    client.post("/api/v1/games", json={"player_1": "Alice", "player_2": "Bob", "board_size": 10})

    game = game_service.get_game(settings.default_uuid)
    for board in game.boards.values():
        board.grid = {Coordinate(x, y): CellState.WATER for x in range(10) for y in range(10)}
        board.ships = []

    resp1 = client.post("/api/v1/games/moves", json={"x": 0, "y": 0})
    assert resp1.json()["next_player"] == "Bob"

    resp2 = client.post("/api/v1/games/moves", json={"x": 1, "y": 1})
    assert resp2.json()["next_player"] == "Alice"


def test_given_games_api_when_game_is_played_full_then_game_concludes_successfully(
    client: TestClient, game_service: GameService
):
    client.post("/api/v1/games", json={"player_1": "Alice", "player_2": "Bob", "board_size": 10})

    game = game_service.get_game(settings.default_uuid)
    bob_board = game.boards["Bob"]

    bob_board.grid = {Coordinate(x, y): CellState.WATER for x in range(10) for y in range(10)}
    target = Coordinate(0, 0)
    bob_board.grid[target] = CellState.SHIP
    bob_board.ships = [Ship(cells={target}, hits=set())]

    response = client.post("/api/v1/games/moves", json={"x": 0, "y": 0})
    assert response.json()["result"].lower() == "sunk"

    blocked_resp = client.post("/api/v1/games/moves", json={"x": 1, "y": 1})
    assert blocked_resp.status_code == 404
