from services.game_service import GameService

_game_service: GameService = GameService()


# Have a singleton service for now, with database this would be per request instance
def get_game_service() -> GameService:
    return _game_service
