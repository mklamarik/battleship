from uuid import UUID

from pydantic import BaseModel, Field

from core.types import GamePhase, ShotResult


class CreateGameRequest(BaseModel):
    player_1: str
    player_2: str
    board_size: int = Field(ge=10, le=20)


class CreateGameResponse(BaseModel):
    game_id: UUID
    current_player: str
    status: GamePhase


class MoveRequest(BaseModel):
    x: int
    y: int


class MoveResponse(BaseModel):
    result: ShotResult
    next_player: str


class GameStateResponse(BaseModel):
    game_id: UUID
    players: list[str]
    board_size: int
    current_player: str
    status: GamePhase
