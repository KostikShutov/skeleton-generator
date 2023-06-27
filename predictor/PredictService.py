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

    def predict(self, course: list[Coordinate]) -> list[object]:
        result: list[object] = []
        course: list[Coordinate] = self.__prepareCoordinates(course)
        parts: list[list[Coordinate]] = self.__createParts(course)

        for part in parts:
            flattenX: list[list[float, float]] = self.coordinatesTransformer.flatten(part)
            commands: list[object] = self.__doPredict(flattenX)

            logging.debug('Predict x: %s' % [str(c) for c in part])
            logging.debug('     to y: %s' % [str(c) for c in commands])

            result += commands

        return result

    def __prepareCoordinates(self, course: list[Coordinate]) -> list[Coordinate]:
        course: list[Coordinate] = self.interpolateService.interpolate(course)

        self.coordinatesLogger.log(
            coordinates=course,
            key='course',
        )

        return course

    def __createParts(self, coordinates: list[Coordinate]) -> list[list[Coordinate]]:
        result: list[list[Coordinate]] = []
        parts: list[list[Coordinate]] = self.coordinatesTransformer.splitToParts(coordinates)

        for part in parts:
            self.coordinatesLogger.log(
                coordinates=part,
                key='part',
            )

            normalized: list[Coordinate] = self.coordinatesTransformer.normalizeToZero(part)

            self.coordinatesLogger.log(
                coordinates=normalized,
                key='normalized',
            )

            result.append(normalized)

        return result

    def __doPredict(self, flattenX: list[list[float]]) -> list[object]:
        result: list[object] = []
        prediction: any = self.__loadModel().predict(tf.expand_dims(flattenX, axis=0))
        commands: list[list[float, float, float]] = prediction[0].tolist()

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
