from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int

    def neighbors(self) -> set[Coordinate]:
        return {
            Coordinate(self.x + dx, self.y + dy)
            for dx in (-1, 0, 1)
            for dy in (-1, 0, 1)
            if not (dx == 0 and dy == 0)
        }
