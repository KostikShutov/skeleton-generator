import logging
import tensorflow as tf
from keras.models import model_from_json
from keras.models import Sequential
from common.commands.Command import Command
from common.coordinates.Coordinate import Coordinate
from common.coordinates.CoordinatesLogger import CoordinatesLogger
from common.coordinates.CoordinatesService import CoordinatesService
from common.interpolation.InterpolateService import InterpolateService


class CommandsPredictor:
    def __init__(self, coordinatesLogger: CoordinatesLogger,
                 coordinatesService: CoordinatesService,
                 interpolateService: InterpolateService) -> None:
        self.coordinatesLogger = coordinatesLogger
        self.coordinatesService = coordinatesService
        self.interpolateService = interpolateService

    def predict(self, coordinates: list[Coordinate]) -> list[Command]:
        coordinates = self.__prepareCoordinates(coordinates)
        parts: list[list[Coordinate]] = self.coordinatesService.splitToParts(coordinates)
        commands: list[Command] = []

        for part in parts:
            flattenX: list[float] = self.coordinatesService.flattenWithRound(part)
            flattenY: list[float, float] = self.__doPredict(flattenX)

            logging.debug('Predict x part: %s' % flattenX)
            logging.debug('Predict y part: %s' % flattenY)

            commands.append(Command(flattenY[0], flattenY[1]))

        return commands

    def __prepareCoordinates(self, coordinates: list[Coordinate]) -> list[Coordinate]:
        coordinatesOld: list[Coordinate] = self.coordinatesService.normalizeToZero(coordinates)
        coordinatesNew: list[Coordinate] = self.interpolateService.interpolateByModel(coordinatesOld)
        coordinatesNewX, coordinatesNewY, _ = self.interpolateService.interpolateBySplines(coordinatesNew)
        coordinatesNew = self.coordinatesService.combineFromFloatLists(coordinatesNewX, coordinatesNewY)
        coordinatesNew = self.coordinatesService.normalizeToZero(coordinatesNew)

        self.coordinatesLogger.log(coordinatesOld, coordinatesNew, 'interpolation')

        return coordinatesNew

    def __doPredict(self, flattenX: list[float]) -> list[float, float]:
        prediction: any = self.__loadModel().predict(tf.expand_dims(flattenX, axis=0))[0]

        return [float(prediction[0]), float(prediction[1])]

    def __loadModel(self) -> Sequential:
        with open('model/model.json', 'r') as file:
            json: str = file.read()

        model: Sequential = model_from_json(json)
        model.load_weights('model/model.h5')

        return model
