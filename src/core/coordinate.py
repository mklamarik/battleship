from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int

    def neighbors(self) -> set[Coordinate]:
        return {
            Coordinate(self.x + x_offset, self.y + y_offset)
            for x_offset in (-1, 0, 1)
            for y_offset in (-1, 0, 1)
            if not (x_offset == 0 and y_offset == 0)  # we already have center
        }
