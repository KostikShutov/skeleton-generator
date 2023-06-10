from common.coordinates.Coordinate import Coordinate


class CoordinatesTransformer:
    def separateToFloatLists(self, coordinates: list[Coordinate]) -> tuple[list[float], list[float]]:
        coordinatesX: list[float] = []
        coordinatesY: list[float] = []

        for coordinate in coordinates:
            coordinatesX.append(coordinate.x)
            coordinatesY.append(coordinate.y)

        return coordinatesX, coordinatesY

    def combineFromFloatLists(self, coordinatesX: list[float], coordinatesY: list[float]) -> list[Coordinate]:
        coordinates: list[Coordinate] = []

        for i in range(min(len(coordinatesX), len(coordinatesY))):
            coordinates.append(Coordinate(coordinatesX[i], coordinatesY[i]))

        return coordinates

    def splitToParts(self, coordinates: list[Coordinate]) -> list[list[Coordinate]]:
        parts: list[list[Coordinate]] = []

        for i in range(max(0, len(coordinates) - 2)):
            part: list[Coordinate] = coordinates[i:i + 3]
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
