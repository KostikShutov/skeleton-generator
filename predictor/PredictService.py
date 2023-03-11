import numpy as np
from common.commands.Command import Command
from common.coordinates.Coordinate import Coordinate
from predictor.CommandsPredictor import CommandsPredictor


class PredictService:
    def __init__(self, commandsPredictor: CommandsPredictor):
        self.commandsPredictor = commandsPredictor

    def predict(self, coordinates: list[Coordinate]) -> list[object]:
        result: list[object] = []
        commands: list[Command] = self.commandsPredictor.predict(coordinates)

        for command in commands:
            result.append({
                'name': 'TURN',
                'angle': self.__prepareAngle(command.angle),
            })

            result.append({
                'name': 'FORWARD',
                'duration': self.__prepareDuration(command.distance),
            })

        return result

    def __prepareAngle(self, angle: float) -> float:
        angle: float = float(np.degrees(angle)) / 3

        return float(np.clip(angle, -45, 45))

    def __prepareDuration(self, distance: float) -> float:
        return float(distance / 30)
