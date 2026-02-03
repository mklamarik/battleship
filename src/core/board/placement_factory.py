from typing import Any

from placement import PlacementStrategy
from random_placement import RandomPlacement


class PlacementFactory:
    @staticmethod
    def get_strategy(strategy_type: str, **kwargs: Any) -> PlacementStrategy:
        if strategy_type == "random":
            return RandomPlacement(seed=kwargs.get("seed"))
        # Future: Strategy for manual placement
        return RandomPlacement()
