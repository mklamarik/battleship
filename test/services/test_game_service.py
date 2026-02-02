import pytest

from core.types import ShotResult
from services.game_service import GameService


def test_create_game_initial_state():
    service = GameService()

    game = service.create_game(
        player_1="Alice",
        player_2="Bob",
        board_size=10,
    )

    assert game.players[0] == "Alice"
    assert game.players[1] == "Bob"
    assert game.current_player_index == 0


def test_make_move_switches_player_on_water():
    service = GameService()
    service.create_game("Alice", "Bob", 10)

    result = service.make_move(0, 0)

    assert result == ShotResult.WATER
    assert service.get_game().current_player_index == 1


def test_get_game_without_create_raises():
    service = GameService()

    with pytest.raises(RuntimeError):
        service.get_game()
