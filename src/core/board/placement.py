from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.board.board import Board
    from core.ships.ship_shape import ShipShape


class PlacementStrategy(ABC):
    @abstractmethod
    def place(self, board: "Board", fleet: list["ShipShape"]) -> None: ...
