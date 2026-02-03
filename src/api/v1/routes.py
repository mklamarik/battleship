from uuid import UUID

from fastapi import APIRouter, Depends

from core.settings import settings
from core.types import GamePhase
from debug.dto import DebugBoardDTO, DebugBoardsResponse
from models.dto import (
    CreateGameRequest,
    CreateGameResponse,
    GameStateResponse,
    MoveRequest,
    MoveResponse,
)
from services.dependencies import get_game_service
from services.game_service import GameService

router = APIRouter()

# Remove if games are accessed by session ID in route
DEFAULT_UUID: UUID = settings.default_uuid


@router.post("/games", response_model=CreateGameResponse)
def create_game(
    request: CreateGameRequest, game_service: GameService = Depends(get_game_service)
) -> CreateGameResponse:
    """
    Initialize a new Battleship game session.

    This endpoint creates a new game instance, initializes the game boards,
    and triggers the automatic ship placement strategy.

    Args:
        request: Configuration for the game including player names and board size.
        game_service: Injected singleton handling game persistence.

    Returns:
        CreateGameResponse: Details of the created game and initial state.
    """
    game = game_service.create_game(
        request.player_1,
        request.player_2,
        request.board_size,
    )

    return CreateGameResponse(
        game_id=game.game_id, current_player=game.current_player, status=GamePhase.IN_PROGRESS
    )


# Change to /games/{game_id}/moves for multiple sessions and add it to list of parameters
@router.post("/games/moves", response_model=MoveResponse)
def make_move(
    move: MoveRequest, game_service: GameService = Depends(get_game_service)
) -> MoveResponse:
    """
    Submit a shot coordinate for the current player.

    Processes a shot at the specified (x, y) coordinates. Validates if the move
    is legal based on turn order and board boundaries.

    Returns:
        MoveResponse: The result of the shot (HIT, MISS, SUNK) and the next player's turn.

    Raises:
        InvalidStateError: If the game is not in progress.
        OutOfBoundsError: If coordinates are outside the board dimensions.
        DuplicateShotError: If the coordinate has already been targeted.
    """
    result, next_player = game_service.make_move(DEFAULT_UUID, move.x, move.y)

    return MoveResponse(result=result, next_player=next_player)


# Change to /games/{game_id} for multiple sessions
@router.get("/games", response_model=GameStateResponse)
def get_game_state(game_service: GameService = Depends(get_game_service)) -> GameStateResponse:
    """
    Retrieve the current status and metadata of the active game.

    Used to poll the game state, including the current turn, remaining ship counts,
    and the current phase (SETUP, IN_PROGRESS, or FINISHED(winner)).
    """
    game = game_service.get_game(DEFAULT_UUID)

    return GameStateResponse(
        game_id=DEFAULT_UUID,
        players=game.players,
        board_size=game.board_size,
        current_player=game.current_player,
        status=game.phase,
    )


@router.get(
    "/games/debug/boards",
    response_model=DebugBoardsResponse,
)
def get_debug_boards(
    game_service: GameService = Depends(get_game_service),
) -> DebugBoardsResponse:
    """
    **Development Only**: Fetch full board matrices including ship positions.

    This endpoint bypasses the 'fog of war' and returns the internal representation
    of both players' boards. Useful for testing placement logic and AI behavior.
    """
    boards = game_service.get_debug_boards()

    return DebugBoardsResponse(
        current_player=game_service.get_game(DEFAULT_UUID).current_player,
        players={player: DebugBoardDTO(board=matrix) for player, matrix in boards.items()},
    )
