import logging
import tensorflow as tf
from keras.models import model_from_json
from keras.models import Sequential
from common.commands.Command import Command
from common.coordinates.Coordinate import Coordinate
from common.coordinates.CoordinatesLogger import CoordinatesLogger
from common.coordinates.CoordinatesTransformer import CoordinatesTransformer
from common.interpolation.InterpolateService import InterpolateService


class PredictService:
    def __init__(self, coordinatesLogger: CoordinatesLogger,
                 coordinatesTransformer: CoordinatesTransformer,
                 interpolateService: InterpolateService) -> None:
        self.coordinatesLogger = coordinatesLogger
        self.coordinatesTransformer = coordinatesTransformer
        self.interpolateService = interpolateService

    def predict(self, coordinates: list[Coordinate]) -> list[list[object]]:
        coordinates: list[Coordinate] = self.__prepareCoordinates(coordinates)
        parts: list[list[Coordinate]] = self.__createParts(coordinates)
        result: list[list[object]] = []

        for part in parts:
            flattenX: list[list[float, float]] = self.coordinatesTransformer.flatten(part)
            flattenY: list[object] = self.__doPredict(flattenX)

            logging.debug('Predict x part: %s' % flattenX)
            logging.debug('Predict y part: %s' % flattenY)

            result += flattenY

        return result

    def __prepareCoordinates(self, coordinatesOld: list[Coordinate]) -> list[Coordinate]:
        coordinatesNew: list[Coordinate] = self.interpolateService.interpolateByLinear(coordinatesOld)
        coordinatesNewX, coordinatesNewY, _ = self.interpolateService.interpolateBySplines(coordinatesNew)
        coordinatesNew = self.coordinatesTransformer.combineFromFloatLists(coordinatesNewX, coordinatesNewY)

        self.coordinatesLogger.log(coordinatesOld, coordinatesNew, 'interpolation')

        return coordinatesNew

    def __createParts(self, coordinates: list[Coordinate]) -> list[list[Coordinate]]:
        parts: list[list[Coordinate]] = self.coordinatesTransformer.splitToParts(coordinates)

        return [self.coordinatesTransformer.normalizeToZero(part) for part in parts]

    def __doPredict(self, flattenX: list[list[float]]) -> list[object]:
        prediction: any = self.__loadModel().predict(tf.expand_dims(flattenX, axis=0))[0]
        commands: list[list[float, float, float]] = prediction.tolist()
        result: list[object] = []

        for command in commands:
            command = Command(
                type=Command.TURN if command[0] >= 1.5 else Command.MOVE,
                angle=command[1],
                distance=command[2],
            )

            if command.type == Command.MOVE:
                result.append({
                    'name': 'MOVE',
                    'duration': command.distance,
                })

            if command.type == Command.TURN:
                result.append({
                    'name': 'TURN',
                    'angle': command.angle,
                })

        return result

    def __loadModel(self) -> Sequential:
        with open('model/model.json', 'r') as file:
            json: str = file.read()

        model: Sequential = model_from_json(json)
        model.load_weights('model/model.h5')

        return model
