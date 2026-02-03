class BattleshipError(Exception):
    pass


class DuplicateShotError(BattleshipError):
    pass


class OutOfBoundsError(BattleshipError):
    pass


class InvalidStateError(BattleshipError):
    pass


class PlacementError(BattleshipError):
    pass
