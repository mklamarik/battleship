import logging
from uuid import UUID

from core.board.board import Board
from core.board.placement import PlacementStrategy
from core.ships.ship_shape import ShipShape
from core.state import GameState, Player1TurnState
from core.types import GamePhase, ShotResult

logger = logging.getLogger(__name__)


class Game:
    def __init__(
        self,
        game_id: UUID,
        player_1: str,
        player_2: str,
        board_size: int,
        placement: PlacementStrategy,
        fleet: list[ShipShape],
    ) -> None:
        self.game_id = game_id
        self.players = [player_1, player_2]
        self.board_size = board_size

        self.boards: dict[str, Board] = {
            player_1: Board(self.board_size),
            player_2: Board(self.board_size),
        }

        """
        This would normally be part of its own state (in case of placing) but
        for the sake of simplicity I put it here
        """
        placement.place(self.boards[player_1], fleet)
        placement.place(self.boards[player_2], fleet)
        logger.info("Game initialized, setting turn to player 1")

        self._state: GameState = Player1TurnState()

    def set_state(self, state: "GameState") -> None:
        logger.info(f"Game state set to {state}")
        self._state = state

    @property
    def current_player(self) -> str:
        return self._state.get_active_player(self)

    @property
    def phase(self) -> GamePhase:
        return self._state.get_phase()

    def apply_move(self, x: int, y: int) -> ShotResult:
        return self._state.handle_shot(self, x, y)
