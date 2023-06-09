import os
import math
import json
import logging
import visualkeras
import tensorflow as tf
from datetime import datetime
from collections.abc import Iterable
from keras.models import Sequential
from keras.utils import plot_model
from keras_visualizer import visualizer
from common.commands.Command import Command
from common.commands.CommandsTransformer import CommandsTransformer
from common.coordinates.Coordinate import Coordinate
from common.coordinates.CoordinatesLogger import CoordinatesLogger
from common.coordinates.CoordinatesParser import CoordinatesParser
from common.coordinates.CoordinatesTransformer import CoordinatesTransformer
from common.interpolation.InterpolateService import InterpolateService
from predictor.PredictModel import PredictModel
from trainer.PredictiveController import PredictiveController
from utils.Logger import Logger


class TrainService:
    def __init__(self, coordinatesParser: CoordinatesParser,
                 coordinatesTransformer: CoordinatesTransformer,
                 coordinatesLogger: CoordinatesLogger,
                 commandsTransformer: CommandsTransformer,
                 interpolateService: InterpolateService,
                 predictiveController: PredictiveController) -> None:
        self.coordinatesParser = coordinatesParser
        self.coordinatesTransformer = coordinatesTransformer
        self.coordinatesLogger = coordinatesLogger
        self.commandsTransformer = commandsTransformer
        self.interpolateService = interpolateService
        self.predictiveController = predictiveController

    def train(self) -> None:
        with open('model/train.json', 'r') as file:
            courses: Iterable = json.load(file)

        model: Sequential = PredictModel().getModel()
        trainX: list[list[list[float, float]]] = []
        trainY: list[list[list[int, float, float]]] = []

        for course in courses:
            course: list[Coordinate] = self.coordinatesParser.parse(course)
            items: list[tuple[list[Coordinate], list[Command]]] = self.__createItems(course)

            for part, commands in items:
                flattenX: list[list[float, float]] = self.coordinatesTransformer.flatten(part)
                flattenY: list[list[int, float, float]] = self.commandsTransformer.flatten(commands)

                logging.debug('Train x: %s' % [str(c) for c in part])
                logging.debug('   to y: %s' % [str(c) for c in commands])

                trainX.append(flattenX)
                trainY.append(flattenY)

        tensorboard_dir: str = Logger.DIR + '/tensorboard/' + datetime.now().strftime('%Y-%m-%d_%H:%M:%S.%f')
        tensorboard_callback: any = tf.keras.callbacks.TensorBoard(log_dir=tensorboard_dir, histogram_freq=1)

        model.fit(x=trainX,
                  y=trainY,
                  epochs=64,
                  batch_size=60,
                  callbacks=[tensorboard_callback])

        self.__saveModel(model)

    def __createItems(self, course: list[Coordinate]) -> list[tuple[list[Coordinate], list[Command]]]:
        result: list[tuple[list[Coordinate], list[Command]]] = []
        course: list[Coordinate] = self.interpolateService.interpolate(course)
        parts: list[list[Coordinate]] = self.coordinatesTransformer.splitToParts(course)

        additional: str = self.coordinatesLogger.log(
            coordinates=course,
            tag='course',
        )

        for part in parts:
            part: list[Coordinate] = self.predictiveController.calculateTrajectory(part)

            self.coordinatesLogger.log(
                coordinates=part,
                tag='part',
                additional=additional,
            )

            commands: list[Command] = [
                Command(Command.TURN, angle=self.__calculateAngle(part)),
                Command(Command.MOVE, distance=self.__calculateDistance(part)),
            ]

            normalized: list[Coordinate] = self.coordinatesTransformer.normalizeToZero(part)

            self.coordinatesLogger.log(
                coordinates=normalized,
                tag='normalized',
                additional=additional,
            )

            result.append((normalized, commands))

        return result

    def __calculateAngle(self, part: list[Coordinate]) -> float:
        return part[2].angle

    def __calculateDistance(self, part: list[Coordinate]) -> float:
        distance: float = 0.0

        for i in range(max(0, len(part) - 1)):
            first: Coordinate = part[i]
            second: Coordinate = part[i + 1]
            distance += math.hypot(second.x - first.x, second.y - first.y)

        return float(distance / 15)

    def __saveModel(self, model: Sequential) -> None:
        json: str = model.to_json()

        with open('model/model.json', 'w') as file:
            file.write(json)

        model.save_weights('model/model.h5')
        plot_model(model, to_file='model/model.png', show_shapes=True, show_layer_names=False)
        visualizer(model, file_name='model/graph', file_format='png')
        os.remove('model/graph')
        visualkeras.layered_view(model, legend=True, to_file='model/view.png')
