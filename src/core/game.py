from uuid import UUID, uuid4

from core.state import GameOverState, GameState, InitializingState, PlayerTurnState
from core.types import GameStatus, ShotResult


class Game:
    def __init__(self, player_1: str, player_2: str, board_size: int):
        self.id: UUID = uuid4()
        self.player_1 = player_1
        self.player_2 = player_2
        self.board_size = board_size

        self.current_player = player_1
        self.state: GameState = InitializingState()

    def status(self) -> GameStatus:
        return (
            GameStatus.ONGOING if not isinstance(self.state, GameOverState) else GameStatus.FINISHED
        )

    def start(self) -> None:
        self.state = PlayerTurnState()

    def make_move(self, x: int, y: int) -> ShotResult:
        return self.state.handle_move(self, x, y)

    def other_player(self) -> str:
        return self.player_2 if self.current_player == self.player_1 else self.player_1

    def end_game(self) -> None:
        self.state = GameOverState()
