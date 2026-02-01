from uuid import UUID

from fastapi import APIRouter, Depends

from core.types import GameStatus
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
        game_id=game.id,
        current_player=game.current_player,
        status=GameStatus.ONGOING,
    )


@router.post("/games/{game_id}/moves", response_model=MoveResponse)
def make_move(
    game_id: UUID, move: MoveRequest, game_service: GameService = Depends(get_game_service)
) -> MoveResponse:
    result = game_service.make_move(move.x, move.y)
    game = game_service.get_game()

    return MoveResponse(
        result=result,
        next_player=game.current_player,
    )


@router.get("/games/{game_id}", response_model=GameStateResponse)
def get_game_state(
    game_id: UUID, game_service: GameService = Depends(get_game_service)
) -> GameStateResponse:
    game = game_service.get_game()

    return GameStateResponse(
        game_id=game.id,
        players=[game.player_1, game.player_2],
        board_size=game.board_size,
        current_player=game.current_player,
        status=game.state.name(),
    )
