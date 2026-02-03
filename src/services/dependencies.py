from services.game_service import GameService

_game_service: GameService | None = None


# Have a singleton service for now, with database this would be per request
def get_game_service() -> GameService:
    global _game_service

    if _game_service is None:
        _game_service = GameService()

    return _game_service
