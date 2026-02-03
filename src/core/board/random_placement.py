import logging
import random

from core.board.board import Board
from core.board.placement import PlacementStrategy
from core.coordinate import Coordinate
from core.ships.ship import Ship
from core.ships.ship_shape import ShipShape
from core.types import CellState

logger = logging.getLogger(__name__)


class RandomPlacement(PlacementStrategy):
    def __init__(self, seed: int | None = None) -> None:
        self._rng = random.Random(seed)

    def place(self, board: Board, fleet: list[ShipShape]) -> None:
        for shape in fleet:
            self._place_ship_shape(board, shape)

    def _place_ship_shape(self, board: Board, shape: ShipShape) -> None:
        max_attempts = 1000
        rotations = list(self._all_rotations(shape))

        for attempt in range(max_attempts):
            logger.debug(f"Placement attempt {attempt} for ship shape {shape}")
            origin = Coordinate(self._rng.randrange(board.size), self._rng.randrange(board.size))
            rotated_shape = self._rng.choice(rotations)

            cells = {Coordinate(origin.x + c.x, origin.y + c.y) for c in rotated_shape.cells}

            if self._is_valid(board, cells):
                ship = Ship(cells=cells, hits=set())
                board.ships.append(ship)
                for cell in cells:
                    board.grid[cell] = CellState.SHIP
                return

        logging.error(f"Failed to place ship after {max_attempts}")
        raise RuntimeError("Failed to place ship")

    def _is_valid(self, board: Board, cells: set[Coordinate]) -> bool:
        return (
            self._in_bounds(board, cells)
            and not self._overlaps(board, cells)
            and not self._touches(board, cells)
        )

    def _in_bounds(self, board: Board, cells: set[Coordinate]) -> bool:
        return all(0 <= cell.x < board.size and 0 <= cell.y < board.size for cell in cells)

    def _overlaps(self, board: Board, cells: set[Coordinate]) -> bool:
        return any(board.grid[cell] != CellState.WATER for cell in cells)

    def _touches(self, board: Board, cells: set[Coordinate]) -> bool:
        for cell in cells:
            for neighbor in cell.neighbors():
                if not (0 <= neighbor.x < board.size and 0 <= neighbor.y < board.size):
                    continue
                if neighbor in cells:
                    continue
                if board.grid[neighbor] == CellState.SHIP:
                    return True
        return False

    def _all_rotations(self, shape: ShipShape) -> set[ShipShape]:
        rotations = {shape}
        current = shape
        for _ in range(3):
            current = current.rotated()
            rotations.add(current)
        return rotations
