from core.game import Game
from core.types import ShotResult


def handle_move(game: Game, x: int, y: int) -> ShotResult:
    result = game.apply_move(x, y)

    if result == ShotResult.WATER:
        game.switch_player()

    return result
