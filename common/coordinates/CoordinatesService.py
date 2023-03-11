from common.coordinates.Coordinate import Coordinate


class CoordinatesService:
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
            part: list[Coordinate] = self.normalizeToZero(coordinates[i:i + 3])
            parts.append(part)

        return parts

    def normalizeToZero(self, coordinates: list[Coordinate]) -> list[Coordinate]:
        if len(coordinates) == 0:
            return []

        first: Coordinate = coordinates[0]
        normalized: list[Coordinate] = []

        for coordinate in coordinates:
            normalized.append(Coordinate(
                round(coordinate.x - first.x, 2),
                round(coordinate.y - first.y, 2),
                coordinate.angle,
            ))

        return normalized

    def flattenWithRound(self, coordinates: list[Coordinate]) -> list[float]:
        flattened: list[float] = []

        for coordinate in coordinates:
            flattened.append(round(coordinate.x, 2))
            flattened.append(round(coordinate.y, 2))

        return flattened
