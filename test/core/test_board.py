import pytest

from core.board import Board
from core.coordinate import Coordinate
from core.ship import Ship
from core.types import CellState, ShotResult


def make_board_with_ship(size: int, ship_cells: set[Coordinate]) -> Board:
    """
    Create a board with a deterministic ship placement.
    """
    board = Board(size)

    # Reset random initialization
    board.grid = {Coordinate(x, y): CellState.WATER for x in range(size) for y in range(size)}
    board.ships = []

    ship = Ship(cells=ship_cells, hits=set())
    board.ships.append(ship)

    for coord in ship_cells:
        board.grid[coord] = CellState.SHIP

    return board


def test_shoot_empty_cell_returns_water():
    board = make_board_with_ship(
        size=5,
        ship_cells={Coordinate(2, 2)},
    )

    result = board.shoot(0, 0)

    assert result == ShotResult.WATER
    assert board.grid[Coordinate(0, 0)] == CellState.MISS


def test_shoot_ship_cell_returns_hit():
    board = make_board_with_ship(
        size=5,
        ship_cells={Coordinate(1, 1), Coordinate(1, 2)},
    )

    result = board.shoot(1, 1)

    assert result == ShotResult.HIT
    assert board.grid[Coordinate(1, 1)] == CellState.HIT


def test_shooting_all_ship_cells_sinks_ship():
    ship_cells = {Coordinate(1, 1), Coordinate(1, 2)}

    board = make_board_with_ship(
        size=5,
        ship_cells=ship_cells,
    )

    board.shoot(1, 1)
    result = board.shoot(1, 2)

    assert result == ShotResult.SUNK
    assert board.all_ships_sunk() is True


def test_shooting_same_cell_twice_raises():
    board = make_board_with_ship(
        size=5,
        ship_cells={Coordinate(2, 2)},
    )

    board.shoot(2, 2)

    with pytest.raises(ValueError):
        board.shoot(2, 2)


def test_shoot_out_of_bounds_raises():
    board = make_board_with_ship(
        size=5,
        ship_cells={Coordinate(2, 2)},
    )

    with pytest.raises(ValueError):
        board.shoot(-1, 0)

    with pytest.raises(ValueError):
        board.shoot(5, 5)
