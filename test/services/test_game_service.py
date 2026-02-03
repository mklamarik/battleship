import pytest

from core.board.placement import PlacementStrategy
from core.coordinate import Coordinate
from core.settings import settings
from core.ships.ship import Ship
from core.types import CellState, ShotResult
from services.game_service import GameService

DEFAULT_UUID = settings.default_uuid


def test_given_create_game_when_game_is_created_then_game_is_set_up_correctly():
    service = GameService()
    game = service.create_game(player_1="Alice", player_2="Bob", board_size=10)

    assert game.players[0] == "Alice"
    assert game.players[1] == "Bob"
    assert game.board_size == 10


def test_given_make_move_when_player_hits_water_then_players_switch_turn(
    empty_placement: PlacementStrategy,
):
    service = GameService()
    # Inject empty placement: (0,0) is guaranteed water
    service.create_game("Alice", "Bob", 10, placement_strategy=empty_placement)

    result, next_player = service.make_move(DEFAULT_UUID, 0, 0)

    assert result == ShotResult.WATER
    assert next_player == "Bob"


def test_given_make_move_when_player_hits_or_sinks_then_player_turn_repeats(
    empty_placement: PlacementStrategy,
):
    service = GameService()
    game = service.create_game("Alice", "Bob", 10, placement_strategy=empty_placement)

    target = Coordinate(2, 2)
    game.boards["Bob"].grid[target] = CellState.SHIP
    game.boards["Bob"].ships.append(Ship(cells={target}, hits=set()))

    target = Coordinate(5, 5)
    game.boards["Bob"].grid[target] = CellState.SHIP
    game.boards["Bob"].ships.append(Ship(cells={target}, hits=set()))

    result, next_player = service.make_move(DEFAULT_UUID, 5, 5)

    assert result == ShotResult.SUNK
    assert next_player == "Alice"


def test_given_get_game_when_create_game_wasnt_called_then_get_game_raises_error():
    service = GameService()
    with pytest.raises(RuntimeError):
        service.get_game(DEFAULT_UUID)
