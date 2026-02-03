import logging
import os
import threading
from uuid import UUID

from core.board.placement import PlacementStrategy
from core.board.random_placement import RandomPlacement
from core.game import Game
from core.settings import settings
from core.ships.fleet_factory import FleetFactory
from core.ships.ship_shape import ShipShape
from core.types import ShotResult
from debug.board_view import board_to_matrix

logger = logging.getLogger(__name__)


class GameService:
    def __init__(self) -> None:
        self._default_uuid: UUID = settings.default_uuid
        self._games: dict[UUID, Game] = {}
        self._lock = threading.Lock()

    def create_game(
        self,
        player_1: str,
        player_2: str,
        board_size: int,
        placement_strategy: PlacementStrategy | None = None,
        fleet: list[ShipShape] | None = None,
    ) -> Game:
        seed_env = os.getenv("GAME_SEED")
        seed = int(seed_env) if seed_env else None
        # This can get replaced by injecting it from the router if manual placement is required
        placement_strategy = placement_strategy or RandomPlacement(seed=seed)
        fleet = fleet or FleetFactory.get_standard_fleet()

        game_id = self._default_uuid  # Replace with real uuid logic to accomodate for sessions
        game = Game(game_id, player_1, player_2, board_size, placement_strategy, fleet)
        logger.info(f"Game created for ID {self._default_uuid}")

        # Ensure spam calls don't try to access the same in-memory dict
        with self._lock:
            self._games[game_id] = game
        return game

    def make_move(self, game_id: UUID, x: int, y: int) -> tuple[ShotResult, str]:
        """
        This is the best countermeasure for spamming turns by the same player for now.
        There is still an issue of a player performing a hit as another player.
        This however cannot be resolved without proper user management, which is out of scope
        for this assignment.
        """
        with self._lock:
            game = self._games.get(game_id)
            if not game:
                raise KeyError("Game not found")
            move_player: str = game.current_player
            logger.info(f"Move requested by player {move_player} at {x}, {y} for ID {game_id}")

            result = game.apply_move(x, y)
            logger.info(
                f"Player {move_player} move at {x}, {y} for ID {self._default_uuid} with {result}"
            )
            return result, game.current_player

    def get_game(self, game_id: UUID) -> Game:
        if not self._games:
            raise RuntimeError("Game not found")

        return self._games[game_id]

    def get_debug_boards(self, game_id: UUID = settings.default_uuid) -> dict[str, list[list[str]]]:
        game = self.get_game(game_id)

        return {player: board_to_matrix(board) for player, board in game.boards.items()}
