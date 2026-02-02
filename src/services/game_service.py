from uuid import UUID

from core.game import Game
from core.transitions import handle_move
from core.types import ShotResult


class GameService:
    def __init__(self) -> None:
        # Keep the UUID at 0, allowing flexibility for multiple sessions later
        self._default_uuid: UUID = UUID("{00000000-0000-0000-0000-000000000000}")
        self._games: dict[UUID, Game] | None = None

    def create_game(self, player_1: str, player_2: str, board_size: int) -> Game:
        game = Game(self._default_uuid, player_1, player_2, board_size)
        game.start()
        if self._games is None:
            self._games = {}
        self._games[self._default_uuid] = game
        return game

    def make_move(self, x: int, y: int) -> ShotResult:
        if self._games is None:
            raise RuntimeError("Game not found")

        return handle_move(self._games[self._default_uuid], x, y)

    def get_game(self) -> Game:
        if self._games is None:
            raise RuntimeError("Game not found")

        return self._games[self._default_uuid]
