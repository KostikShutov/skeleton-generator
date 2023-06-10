import math
import logging
from common.commands.Command import Command
from common.coordinates.Coordinate import Coordinate
from common.coordinates.CoordinatesLogger import CoordinatesLogger
from common.coordinates.CoordinatesTransformer import CoordinatesTransformer
from trainer.PredictiveController import PredictiveController


class CommandsCreator:
    def __init__(self, coordinatesLogger: CoordinatesLogger,
                 coordinatesTransformer: CoordinatesTransformer,
                 predictiveController: PredictiveController) -> None:
        self.coordinatesLogger = coordinatesLogger
        self.coordinatesTransformer = coordinatesTransformer
        self.predictiveController = predictiveController

    def create(self, course: list[Coordinate]) -> list[tuple[list[Coordinate], list[Command]]]:
        trajectory: list[Coordinate] = self.predictiveController.calculateTrajectory(course)

        self.coordinatesLogger.log(course, trajectory, 'simulation')
        logging.debug('Trajectory: %s' % [[c.x, c.y, c.angle] for c in trajectory])

        result: list[tuple[list[Coordinate], list[Command]]] = []
        parts: list[list[Coordinate]] = self.coordinatesTransformer.splitToParts(trajectory)

        for part in parts:
            result.append(self.__createItem(part))

        return result

    def __createItem(self, part: list[Coordinate]) -> tuple[list[Coordinate], list[Command]]:
        commands: list[Command] = [
            Command(Command.TURN, angle=self.__calculateAngle(part)),
            Command(Command.MOVE, distance=self.__calculateDistance(part)),
        ]

        part = self.coordinatesTransformer.normalizeToZero(part)

        return part, commands

    def __calculateAngle(self, part: list[Coordinate]) -> float:
        return part[0].angle

    def __calculateDistance(self, part: list[Coordinate]) -> float:
        distance: float = 0.0

        for i in range(max(0, len(part) - 1)):
            first: Coordinate = part[i]
            second: Coordinate = part[i + 1]
            distance += math.hypot(second.x - first.x, second.y - first.y)

        return float(distance / 15)
