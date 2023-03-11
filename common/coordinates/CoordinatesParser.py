from collections.abc import Iterable
from common.coordinates.Coordinate import Coordinate


class CoordinatesParser:
    def parse(self, data: Iterable) -> list[Coordinate]:
        coordinates: list[Coordinate] = []

        for item in data:
            x: float = float(item['x'])
            y: float = float(item['y'])
            coordinates.append(Coordinate(x, y))

        return coordinates
