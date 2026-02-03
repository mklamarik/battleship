from core.ships.ship_shape import ShipShape
from core.ships.ship_shapes import CROSS, DOUBLE, L_SHAPE, SINGLE, TRIPLE


class FleetFactory:
    @staticmethod
    def get_standard_fleet() -> list[ShipShape]:
        return [
            L_SHAPE,
            CROSS,
            TRIPLE,
            DOUBLE,
            DOUBLE,
            SINGLE,
            SINGLE,
        ]

    @staticmethod
    def get_test_fleet() -> list[ShipShape]:
        return [SINGLE]

    @staticmethod
    def get_test_inorder_fleet() -> list[ShipShape]:
        return [
            SINGLE,
            SINGLE,
            DOUBLE,
            DOUBLE,
            TRIPLE,
            CROSS,
            L_SHAPE,
        ]
