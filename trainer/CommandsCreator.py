import math
import logging
from common.commands.Command import Command
from common.coordinates.Coordinate import Coordinate
from common.coordinates.CoordinatesLogger import CoordinatesLogger
from common.coordinates.CoordinatesService import CoordinatesService
from trainer.StanleyController import StanleyController


class CommandsCreator:
    def __init__(self, coordinatesLogger: CoordinatesLogger,
                 coordinatesService: CoordinatesService,
                 stanleyController: StanleyController) -> None:
        self.coordinatesLogger = coordinatesLogger
        self.coordinatesService = coordinatesService
        self.stanleyController = stanleyController

    def create(self, course: list[Coordinate]) -> list[tuple[list[Coordinate], Command]]:
        course: list[Coordinate] = self.coordinatesService.normalizeToZero(course)
        trajectory: list[Coordinate] = self.__predictTrajectory(course)

        self.coordinatesLogger.log(course, trajectory, 'simulation')
        logging.debug('Trajectory: %s' % [[c.x, c.y, c.angle] for c in trajectory])

        commands: list[tuple[list[Coordinate], Command]] = []
        parts: list[list[Coordinate]] = self.coordinatesService.splitToParts(trajectory)

        for part in parts:
            angle: float = self.__calculateAngle(part)
            distance: float = self.__calculateDistance(part)
            commands.append((part, Command(angle, distance)))

        return commands

    def __predictTrajectory(self, course: list[Coordinate]) -> list[Coordinate]:
        trajectory: list[Coordinate] = self.stanleyController.predictTrajectory(course)

        return self.coordinatesService.normalizeToZero(trajectory)

    def __calculateAngle(self, part: list[Coordinate]) -> float:
        return part[0].angle

    def __calculateDistance(self, part: list[Coordinate]) -> float:
        distance: float = 0.0

        for i in range(max(0, len(part) - 1)):
            first: Coordinate = part[i]
            second: Coordinate = part[i + 1]
            distance += math.hypot(second.x - first.x, second.y - first.y)

        return distance
