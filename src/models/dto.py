from uuid import UUID

from pydantic import BaseModel, Field

from core.types import GamePhase, ShotResult


class CreateGameRequest(BaseModel):
    """Data required to initialize a new Battleship session."""

    player_1: str = Field(
        default=..., description="Name of the first player (Attacker)", examples=["Alice"]
    )
    player_2: str = Field(
        default=..., description="Name of the second player (Defender)", examples=["Bob"]
    )
    board_size: int = Field(
        default=10, ge=10, le=20, description="Square grid dimension (N x N). Minimum 10."
    )


class CreateGameResponse(BaseModel):
    """
    Initial state of a successfully created game.
    """

    game_id: UUID = Field(..., description="Unique identifier for the game session")
    current_player: str = Field(..., description="The player assigned the first turn")
    status: GamePhase = Field(
        ..., description="The initial phase of the game (e.g., SETUP or IN_PROGRESS)"
    )


class MoveRequest(BaseModel):
    """
    Target coordinates for a player's shot.
    """

    x: int = Field(..., ge=0, description="The horizontal coordinate (0 to board_size - 1)")
    y: int = Field(..., ge=0, description="The vertical coordinate (0 to board_size - 1)")


class MoveResponse(BaseModel):
    """
    The outcome details after processing a move.
    """

    result: ShotResult = Field(..., description="The result of the shot: HIT, MISS, or SUNK")
    next_player: str = Field(..., description="The player who should act next")


class GameStateResponse(BaseModel):
    """
    Comprehensive snapshot of the current game state.
    """

    game_id: UUID = Field(..., description="Unique identifier for the session")
    players: list[str] = Field(..., description="List of all participating players")
    board_size: int = Field(..., description="The dimensions of the game grid")
    current_player: str = Field(
        ..., description="The player who is currently allowed to take a turn"
    )
    status: GamePhase = Field(..., description="The current lifecycle phase of the game session")
