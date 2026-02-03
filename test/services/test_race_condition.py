import asyncio
import time
from unittest.mock import MagicMock, patch

import pytest

from core.exceptions import DuplicateShotError
from core.types import ShotResult
from services.game_service import GameService


@pytest.mark.asyncio
async def test_given_make_move_when_request_is_spammed_by_same_player_then_cellstate_is_changed(
    game_service: GameService,
):
    game = game_service.create_game("Alice", "Bob", 10)
    game_id = game.game_id

    hits: list[tuple[int, int]] = []

    def mock_receive_shot(x: int, y: int):
        if (x, y) in hits:
            raise DuplicateShotError("Cell already shot")
        time.sleep(0.1)
        hits.append((x, y))
        return ShotResult.HIT

    with patch.object(game.boards["Bob"], "receive_shot", side_effect=mock_receive_shot):

        async def fire(y: int):
            return await asyncio.to_thread(game_service.make_move, game_id, 0, y)

        results = await asyncio.gather(fire(0), fire(0), return_exceptions=True)

    successes = [r for r in results if not isinstance(r, Exception)]
    errors = [r for r in results if isinstance(r, Exception)]

    assert len(successes) == 1
    assert len(errors) == 1


@pytest.mark.asyncio
async def test_given_make_move_if_lock_is_removed_then_cellstate_race_condition_happens(
    game_service: GameService,
):
    game = game_service.create_game("Alice", "Bob", 10)

    # Disable the lock to prove the test can catch the race
    with patch.object(game_service, "_lock", MagicMock()):
        hits: list[tuple[int, int]] = []

        def mock_receive_shot(x: int, y: int):
            if (x, y) in hits:
                raise DuplicateShotError("Already shot")
            time.sleep(0.1)
            hits.append((x, y))
            return ShotResult.HIT

        with patch.object(game.boards["Bob"], "receive_shot", side_effect=mock_receive_shot):

            async def fire():
                return await asyncio.to_thread(game_service.make_move, game.game_id, 0, 0)

            results = await asyncio.gather(fire(), fire(), return_exceptions=True)

    # Both succeed because the lock was removed
    successes = [r for r in results if not isinstance(r, Exception)]
    assert len(successes) == 2
