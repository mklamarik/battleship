from pydantic import BaseModel


class DebugBoardDTO(BaseModel):
    board: list[list[str]]


class DebugBoardsResponse(BaseModel):
    current_player: str
    players: dict[str, DebugBoardDTO]
