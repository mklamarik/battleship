from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, NoReturn

from core.types import GameStatus, ShotResult

if TYPE_CHECKING:
    from core.game import Game


class GameState(ABC):
    @abstractmethod
    def name(self) -> GameStatus:
        pass

    @abstractmethod
    def handle_move(self, game: "Game", x: int, y: int) -> ShotResult:
        pass


class InitializingState(GameState):
    def name(self) -> GameStatus:
        return GameStatus.INITIALIZING

    def handle_move(self, game: "Game", x: int, y: int) -> NoReturn:
        raise ValueError("Game not started yet")


class PlayerTurnState(GameState):
    def name(self) -> GameStatus:
        return GameStatus.ONGOING

    def handle_move(self, game: "Game", x: int, y: int) -> ShotResult:
        # Dummy logic for now: always miss
        result = ShotResult.WATER

        if result == ShotResult.WATER:
            game.current_player = game.other_player()

        return result


class GameOverState(GameState):
    def name(self) -> GameStatus:
        return GameStatus.FINISHED

    def handle_move(self, game: "Game", x: int, y: int) -> NoReturn:
        raise ValueError("Game is already over")
