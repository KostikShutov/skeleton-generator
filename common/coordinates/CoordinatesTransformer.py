from common.coordinates.Coordinate import Coordinate


class CoordinatesTransformer:
    PARTS: int = 3

    def separateToFloatLists(self, coordinates: list[Coordinate]) -> tuple[list[float], list[float], list[float]]:
        x: list[float] = []
        y: list[float] = []
        angles: list[float] = []

        for coordinate in coordinates:
            x.append(coordinate.x)
            y.append(coordinate.y)
            angles.append(coordinate.angle)

        return x, y, angles

    def combineFromFloatLists(self, x: list[float], y: list[float], angles: list[float] = None) -> list[Coordinate]:
        coordinates: list[Coordinate] = []
        length: int = min(len(x), len(y))

        if angles is not None:
            length = min(length, len(angles))

        for i in range(length):
            if angles is None:
                coordinate: Coordinate = Coordinate(x[i], y[i])
            else:
                coordinate: Coordinate = Coordinate(x[i], y[i], angles[i])

            coordinates.append(coordinate)

        return coordinates

    def splitToParts(self, coordinates: list[Coordinate]) -> list[list[Coordinate]]:
        parts: list[list[Coordinate]] = []

        for i in range(max(0, len(coordinates) - (self.PARTS - 1))):
            part: list[Coordinate] = coordinates[i:i + self.PARTS]
            parts.append(part)

        return parts

    def normalizeToZero(self, coordinates: list[Coordinate]) -> list[Coordinate]:
        if len(coordinates) == 0:
            return []

        first: Coordinate = coordinates[0]
        normalized: list[Coordinate] = []

        for coordinate in coordinates:
            normalized.append(Coordinate(
                coordinate.x - first.x,
                coordinate.y - first.y,
                coordinate.angle,
            ))

        normalized.pop(0)

        return normalized

    def flatten(self, coordinates: list[Coordinate]) -> list[list[float, float]]:
        flattened: list[list[float, float]] = []

        for coordinate in coordinates:
            flattened.append([coordinate.x, coordinate.y])

        return flattened
