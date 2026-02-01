from enum import Enum


class ShotResult(Enum):
    WATER = "water"
    HIT = "hit"
    SUNK = "sunk"


class GameStatus(Enum):
    INITIALIZING = "initializing"
    ONGOING = "ongoing"
    FINISHED = "finished"
