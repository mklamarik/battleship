from core.coordinate import Coordinate
from core.ships.ship_shape import ShipShape

SINGLE: ShipShape = ShipShape(frozenset({Coordinate(0, 0)}))

DOUBLE: ShipShape = ShipShape(frozenset({Coordinate(0, 0), Coordinate(1, 0)}))

TRIPLE: ShipShape = ShipShape(
    frozenset({Coordinate(0, 0), Coordinate(1, 0), Coordinate(2, 0)})
)

CROSS: ShipShape = ShipShape(
    frozenset(
        {
            Coordinate(0, 0),
            Coordinate(-1, 1),
            Coordinate(0, 1),
            Coordinate(1, 1),
            Coordinate(0, 2),
        }
    )
)

L_SHAPE: ShipShape = ShipShape(
    frozenset(
        {
            Coordinate(0, 0),
            Coordinate(1, 0),
            Coordinate(2, 0),
            Coordinate(3, 0),
            Coordinate(1, 1),
        }
    )
)
