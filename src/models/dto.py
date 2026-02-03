from uuid import UUID

from pydantic import BaseModel, Field

from core.types import GamePhase, ShotResult


class CreateGameRequest(BaseModel):
    player_1: str
    player_2: str
    board_size: int = Field(ge=10, le=20)  # Input validation for board size


class CreateGameResponse(BaseModel):
    game_id: UUID
    current_player: str
    status: GamePhase


class MoveRequest(BaseModel):
    x: int = Field(ge=0)  # Input validation for coordinates
    y: int = Field(ge=0)


class MoveResponse(BaseModel):
    result: ShotResult
    next_player: str


class GameStateResponse(BaseModel):
    game_id: UUID
    players: list[str]
    board_size: int
    current_player: str
    status: GamePhase
