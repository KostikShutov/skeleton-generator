import numpy as np
from common.coordinates.Coordinate import Coordinate
from common.coordinates.CoordinatesTransformer import CoordinatesTransformer
from common.interpolation.CubicSplineService import CubicSplineService


class InterpolateService:
    DS: float = 2.0

    def __init__(self, coordinatesTransformer: CoordinatesTransformer,
                 cubicSplineService: CubicSplineService) -> None:
        self.coordinatesTransformer = coordinatesTransformer
        self.cubicSplineService = cubicSplineService

    def interpolateByLinear(self, coordinates: list[Coordinate]) -> list[Coordinate]:
        coordinatesX, coordinatesY = self.coordinatesTransformer.separateToFloatLists(coordinates)

        coordinatesNewX = np.linspace(coordinatesX[0], coordinatesX[-1], len(coordinatesX))
        coordinatesNewY = np.interp(coordinatesNewX, coordinatesX, coordinatesY)

        return self.coordinatesTransformer.combineFromFloatLists(coordinatesNewX, coordinatesNewY)

    def interpolateBySplines(self, coordinates: list[Coordinate]) -> tuple[list[float], list[float], list[float]]:
        coordinatesX, coordinatesY = self.coordinatesTransformer.separateToFloatLists(coordinates)

        x, y, yaw, _, _ = self.cubicSplineService.calcSplineCourse(coordinatesX, coordinatesY, ds=self.DS)

        return x, y, yaw
