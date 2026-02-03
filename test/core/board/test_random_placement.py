import pytest

from core.board.board import Board
from core.board.random_placement import RandomPlacement
from core.exceptions import PlacementError
from core.ships.fleet_factory import FleetFactory
from core.types import CellState


def test_given_random_placement_when_place_called_with_set_seed_then_fleet_is_set_correctly() -> (
    None
):
    """Verify that a standard fleet always results in the correct number of ship cells."""
    strategy = RandomPlacement(seed=42)
    fleet = FleetFactory.get_standard_fleet()
    board = Board(size=10)

    strategy.place(board, fleet)

    expected_cells = sum(len(ship.cells) for ship in fleet)
    actual_cells = sum(1 for cell in board.grid.values() if cell == CellState.SHIP)

    assert actual_cells == expected_cells
    assert len(board.ships) == len(fleet)


def test_given_random_placement_when_fleet_small_to_large_then_placement_fails_after_retries() -> (
    None
):
    fleet = FleetFactory.get_test_inorder_fleet()
    failing_seed: int = 377

    board = Board(size=10)

    with pytest.raises(PlacementError):
        strategy = RandomPlacement(failing_seed)
        strategy.place(board, fleet)

    fleet = FleetFactory.get_standard_fleet()
    board = Board(size=10)

    strategy = RandomPlacement(failing_seed)
    strategy.place(board, fleet)

    expected_cells = sum(len(ship.cells) for ship in fleet)
    actual_cells = sum(1 for cell in board.grid.values() if cell == CellState.SHIP)

    assert actual_cells == expected_cells
    assert len(board.ships) == len(fleet)
