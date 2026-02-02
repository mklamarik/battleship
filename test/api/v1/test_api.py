from fastapi.testclient import TestClient


def test_create_game(client: TestClient):
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


def test_make_move(client: TestClient):
    client.post(
        "/api/v1/games",
        json={
            "player_1": "Alice",
            "player_2": "Bob",
            "board_size": 10,
        },
    )

    response = client.post(
        "/api/v1/games/00000000-0000-0000-0000-000000000000/moves",
        json={"x": 0, "y": 0},
    )

    assert response.status_code == 200

    data = response.json()
    assert data["result"] == "water"
    assert data["next_player"] == "Bob"
