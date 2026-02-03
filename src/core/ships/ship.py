from dataclasses import dataclass

from core.coordinate import Coordinate


@dataclass
class Ship:
    cells: set[Coordinate]
    hits: set[Coordinate]

    def is_sunk(self) -> bool:
        return self.cells == self.hits
