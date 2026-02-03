from pydantic import BaseModel, Field


class DebugBoardDTO(BaseModel):
    """
    A raw representation of a single player's board matrix.
    """

    board: list[list[str]] = Field(
        default=...,
        description="A 2D grid where strings represent cell states",
    )


class DebugBoardsResponse(BaseModel):
    """
    Complete diagnostic snapshot of all boards in the game.
    """

    current_player: str = Field(
        default=..., description="The name of the player whose turn it currently is."
    )
    players: dict[str, DebugBoardDTO] = Field(
        default=..., description="A mapping of player names to their full, unhidden board state."
    )
