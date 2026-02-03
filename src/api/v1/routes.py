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
    result, next_player = game_service.make_move(DEFAULT_UUID, move.x, move.y)

    return MoveResponse(result=result, next_player=next_player)


# Change to /games/{game_id} for multiple sessions
@router.get("/games", response_model=GameStateResponse)
def get_game_state(game_service: GameService = Depends(get_game_service)) -> GameStateResponse:
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
    boards = game_service.get_debug_boards()

    return DebugBoardsResponse(
        current_player=game_service.get_game(DEFAULT_UUID).current_player,
        players={player: DebugBoardDTO(board=matrix) for player, matrix in boards.items()},
    )
