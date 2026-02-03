from dataclasses import dataclass

from core.coordinate import Coordinate


@dataclass(frozen=True)
class ShipShape:
    cells: frozenset[Coordinate]

    def rotated(self) -> "ShipShape":
        return ShipShape(frozenset(Coordinate(cell.y, -cell.x) for cell in self.cells))
