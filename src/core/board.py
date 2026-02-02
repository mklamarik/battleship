from __future__ import annotations

import random

from core.coordinate import Coordinate
from core.ship import Ship
from core.types import CellState, ShotResult


class Board:
    def __init__(self, size: int) -> None:
        self.size = size
        self.grid: dict[Coordinate, CellState] = {}
        self.ships: list[Ship] = []

        self._initialize_grid()
        self._place_initial_ship()

    def _initialize_grid(self) -> None:
        for x in range(self.size):
            for y in range(self.size):
                self.grid[Coordinate(x, y)] = CellState.WATER

    def _place_initial_ship(self) -> None:
        coord = Coordinate(
            random.randrange(self.size),
            random.randrange(self.size),
        )

        ship = Ship(cells={coord}, hits=set())
        self.ships.append(ship)
        self.grid[coord] = CellState.SHIP

    def shoot(self, x: int, y: int) -> ShotResult:
        coord = Coordinate(x, y)
        self._validate_coordinate(coord)

        state = self.grid[coord]

        if state in (CellState.HIT, CellState.MISS):
            raise ValueError("Cell already shot")

        if state == CellState.WATER:
            self.grid[coord] = CellState.MISS
            return ShotResult.WATER

        self.grid[coord] = CellState.HIT
        ship = self._find_ship_at(coord)
        ship.hits.add(coord)

        return ShotResult.SUNK if ship.is_sunk() else ShotResult.HIT

    def all_ships_sunk(self) -> bool:
        return all(ship.is_sunk() for ship in self.ships)

    def _validate_coordinate(self, coord: Coordinate) -> None:
        if not (0 <= coord.x < self.size and 0 <= coord.y < self.size):
            raise ValueError("Shot out of bounds")

    def _find_ship_at(self, coord: Coordinate) -> Ship:
        for ship in self.ships:
            if coord in ship.cells:
                return ship
        raise RuntimeError("Invariant violated: ship not found")
