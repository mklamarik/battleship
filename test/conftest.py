from typing import TYPE_CHECKING

import pytest
from fastapi.testclient import TestClient

from core.board.placement import PlacementStrategy
from main import app
from services.dependencies import get_game_service
from services.game_service import GameService

if TYPE_CHECKING:
    from core.board.board import Board
    from core.ships.ship_shape import ShipShape

local_service = GameService()


@pytest.fixture
def client():
    app.dependency_overrides[get_game_service] = lambda: local_service
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def game_service():
    return local_service


class EmptyPlacement(PlacementStrategy):
    def place(self, board: "Board", fleet: list["ShipShape"]) -> None:
        pass


@pytest.fixture
def empty_placement() -> PlacementStrategy:
    return EmptyPlacement()
