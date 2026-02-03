from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from core.types import GamePhase, ShotResult

if TYPE_CHECKING:
    from core.game import Game


class GameState(ABC):
    @abstractmethod
    def handle_shot(self, game: "Game", x: int, y: int) -> ShotResult:
        pass

    @abstractmethod
    def get_active_player(self, game: "Game") -> str:
        pass

    @abstractmethod
    def get_phase(self) -> GamePhase:
        pass


class Player1TurnState(GameState):
    def get_active_player(self, game: "Game") -> str:
        return game.players[0]

    def handle_shot(self, game: "Game", x: int, y: int) -> ShotResult:
        result = game.boards[game.players[1]].receive_shot(x, y)

        if result == ShotResult.WATER:
            game.set_state(Player2TurnState())
        elif game.boards[game.players[1]].all_ships_sunk():
            game.set_state(FinishedState(winner=game.current_player))

        return result

    def get_phase(self) -> GamePhase:
        return GamePhase.IN_PROGRESS


class Player2TurnState(GameState):
    def get_active_player(self, game: "Game") -> str:
        return game.players[1]

    def handle_shot(self, game: "Game", x: int, y: int) -> ShotResult:
        result = game.boards[game.players[0]].receive_shot(x, y)

        if result == ShotResult.WATER:
            game.set_state(Player1TurnState())
        elif game.boards[game.players[0]].all_ships_sunk():
            game.set_state(FinishedState(winner=game.current_player))

        return result

    def get_phase(self) -> GamePhase:
        return GamePhase.IN_PROGRESS


class FinishedState(GameState):
    def __init__(self, winner: str) -> None:
        self.winner = winner

    def get_active_player(self, game: "Game") -> str:
        return f"None (Winner: {self.winner})"

    def handle_shot(self, game: "Game", x: int, y: int) -> ShotResult:
        raise ValueError("Game is already finished. No more moves allowed.")

    def get_phase(self) -> GamePhase:
        return GamePhase.FINISHED
