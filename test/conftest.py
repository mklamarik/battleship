import pytest
from fastapi.testclient import TestClient

from main import app
from services.dependencies import get_game_service
from services.game_service import GameService


@pytest.fixture
def client():
    service = GameService()

    app.dependency_overrides[get_game_service] = lambda: service
    yield TestClient(app)
    app.dependency_overrides.clear()
