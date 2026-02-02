from enum import Enum


class ShotResult(Enum):
    WATER = "water"
    HIT = "hit"
    SUNK = "sunk"


class GamePhase(Enum):
    INITIALIZING = "initializing"
    IN_PROGRESS = "in progress"
    FINISHED = "finished"


class CellState(Enum):
    WATER = "~"
    SHIP = "#"
    HIT = "X"
    MISS = "O"
