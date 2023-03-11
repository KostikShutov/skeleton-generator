import numpy as np
from common.coordinates.Coordinate import Coordinate
from common.coordinates.CoordinatesService import CoordinatesService
from common.interpolation.CubicSplineService import CubicSplineService
from common.interpolation.InterpolateModel import InterpolateModel


class InterpolateService:
    DIFF: float = 2.0
    REPEAT: int = 50
    DS: float = 2.0

    def __init__(self, coordinatesService: CoordinatesService,
                 cubicSplineService: CubicSplineService):
        self.coordinatesService = coordinatesService
        self.cubicSplineService = cubicSplineService

    def interpolateByModel(self, coordinates: list[Coordinate]) -> list[Coordinate]:
        coordinatesX, coordinatesY = self.coordinatesService.separateToFloatLists(coordinates)

        trainX = np.array(coordinatesX).repeat(self.REPEAT)
        trainX += (self.DIFF * np.random.normal(0, self.DIFF, len(trainX)))
        trainY = np.array(coordinatesY).repeat(self.REPEAT)
        trainY += (self.DIFF * np.random.normal(0, self.DIFF, len(trainY)))

        model = InterpolateModel().getModel()
        model.fit(trainX, trainY, epochs=32, batch_size=16)

        coordinatesNewX = self.__generateArray(coordinatesX[0], coordinatesX[-1], len(coordinatesX))
        coordinatesNewY = [p[0] for p in model.predict(coordinatesNewX)]

        return self.coordinatesService.combineFromFloatLists(coordinatesNewX, coordinatesNewY)

    def interpolateBySplines(self, coordinates: list[Coordinate]) -> tuple[list[float], list[float], list[float]]:
        coordinatesX, coordinatesY = self.coordinatesService.separateToFloatLists(coordinates)

        x, y, yaw, _, _ = self.cubicSplineService.calcSplineCourse(coordinatesX, coordinatesY, ds=self.DS)

        return x, y, yaw

    def __generateArray(self, start: float, end: float, length: int) -> list[float]:
        step = (end - start) / (length - 1)

        return [start + i * step for i in range(length)]
