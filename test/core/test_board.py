import pytest

from core.board.board import Board
from core.coordinate import Coordinate
from core.ships.ship import Ship
from core.types import CellState, ShotResult


def make_board_with_ship(size: int, ship_cells: set[Coordinate]) -> Board:
    board = Board(size)

    board.grid = {Coordinate(x, y): CellState.WATER for x in range(size) for y in range(size)}
    board.ships = []

    ship = Ship(cells=ship_cells, hits=set())
    board.ships.append(ship)

    for coord in ship_cells:
        board.grid[coord] = CellState.SHIP

    return board


def test_given_receive_shot_when_water_is_hit_then_cellstate_is_set_to_miss():
    board = make_board_with_ship(size=5, ship_cells={Coordinate(2, 2)})

    result = board.receive_shot(0, 0)

    assert result == ShotResult.WATER
    assert board.grid[Coordinate(0, 0)] == CellState.MISS


def test_given_receive_shot_when_ship_is_hit_then_cellstate_is_set_to_hit():
    board = make_board_with_ship(size=5, ship_cells={Coordinate(1, 1), Coordinate(1, 2)})

    result = board.receive_shot(1, 1)

    assert result == ShotResult.HIT
    assert board.grid[Coordinate(1, 1)] == CellState.HIT


def test_given_receive_shot_when_ship_is_sunk_then_result_is_sunk():
    ship_cells = {Coordinate(1, 1), Coordinate(1, 2)}

    board = make_board_with_ship(size=5, ship_cells=ship_cells)

    board.receive_shot(1, 1)
    result = board.receive_shot(1, 2)

    assert result == ShotResult.SUNK
    assert board.all_ships_sunk() is True


def test_given_receive_shot_when_same_cell_is_hit_then_second_hit_raises_error():
    board = make_board_with_ship(size=5, ship_cells={Coordinate(2, 2)})

    board.receive_shot(2, 2)

    with pytest.raises(ValueError):
        board.receive_shot(2, 2)


def test_given_receive_shot_when_coordinates_out_of_bounds_then_board_raises_error():
    board = make_board_with_ship(size=5, ship_cells={Coordinate(2, 2)})

    with pytest.raises(ValueError):
        board.receive_shot(-1, 0)

    with pytest.raises(ValueError):
        board.receive_shot(5, 5)
