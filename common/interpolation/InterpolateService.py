import numpy as np
from common.coordinates.Coordinate import Coordinate
from common.coordinates.CoordinatesTransformer import CoordinatesTransformer
from common.interpolation.CubicSplineService import CubicSplineService


class InterpolateService:
    DS: float = 4.0

    def __init__(self, coordinatesTransformer: CoordinatesTransformer,
                 cubicSplineService: CubicSplineService) -> None:
        self.coordinatesTransformer = coordinatesTransformer
        self.cubicSplineService = cubicSplineService

    def interpolate(self, coordinates: list[Coordinate]) -> list[Coordinate]:
        coordinates: list[Coordinate] = self.__interpolateByLinear(coordinates)
        coordinates: list[Coordinate] = self.__interpolateBySplines(coordinates)

        return coordinates

    def __interpolateByLinear(self, coordinates: list[Coordinate]) -> list[Coordinate]:
        oldX, oldY, _ = self.coordinatesTransformer.separateToFloatLists(coordinates)

        newX = np.arange(oldX[0], oldX[-1], self.DS)
        newY = np.interp(newX, oldX, oldY)

        return self.coordinatesTransformer.combineFromFloatLists(newX, newY)

    def __interpolateBySplines(self, coordinates: list[Coordinate]) -> list[Coordinate]:
        x, y, _ = self.coordinatesTransformer.separateToFloatLists(coordinates)
        x, y, yaw, _, _ = self.cubicSplineService.calcSplineCourse(x, y, ds=self.DS)

        return self.coordinatesTransformer.combineFromFloatLists(x, y, yaw)
