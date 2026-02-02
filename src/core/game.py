from uuid import UUID

from core.board import Board
from core.types import GamePhase, ShotResult


class Game:
    def __init__(self, game_id: UUID, player_1: str, player_2: str, board_size: int) -> None:
        self.game_id: UUID = game_id
        self.players: list[str] = [player_1, player_2]
        self.board_size: int = board_size
        self.current_player_index = 0
        self.phase: GamePhase = GamePhase.INITIALIZING

        self.boards: dict[str, Board] = {
            player_1: Board(self.board_size),
            player_2: Board(self.board_size),
        }

    @property
    def current_player(self) -> str:
        return self.players[self.current_player_index]

    def opponent(self) -> str:
        return self.players[1 - self.current_player_index]

    def switch_player(self) -> None:
        self.current_player_index = 1 - self.current_player_index

    def start(self) -> None:
        if self.phase != GamePhase.INITIALIZING:
            raise RuntimeError("Game already started")

        self.phase = GamePhase.IN_PROGRESS

    def apply_move(self, x: int, y: int) -> ShotResult:
        if self.phase != GamePhase.IN_PROGRESS:
            raise RuntimeError("Game not in progress")

        board = self.boards[self.opponent()]
        result = board.shoot(x, y)

        if not board.all_ships_sunk():
            self.phase = GamePhase.FINISHED

        return result
