from core.game import Game
from core.types import ShotResult


class GameService:
    def __init__(self):
        self._game: Game | None = None

    def create_game(self, player_1: str, player_2: str, board_size: int) -> Game:
        game = Game(player_1, player_2, board_size)
        game.start()
        self._game = game
        return game

    def get_game(self) -> Game:
        if self._game is None:
            raise ValueError("No game exists")
        return self._game

    def make_move(self, x: int, y: int) -> ShotResult:
        game = self.get_game()
        return game.make_move(x, y)
