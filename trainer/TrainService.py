import os
import math
import json
import logging
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
from predictor.PredictModel import PredictModel
from trainer.PredictiveController import PredictiveController
from utils.Logger import Logger


class TrainService:
    def __init__(self, coordinatesParser: CoordinatesParser,
                 coordinatesTransformer: CoordinatesTransformer,
                 coordinatesLogger: CoordinatesLogger,
                 commandsTransformer: CommandsTransformer,
                 predictiveController: PredictiveController) -> None:
        self.coordinatesParser = coordinatesParser
        self.coordinatesTransformer = coordinatesTransformer
        self.coordinatesLogger = coordinatesLogger
        self.commandsTransformer = commandsTransformer
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
        tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=tensorboard_dir, histogram_freq=1)

        model.fit(x=trainX,
                  y=trainY,
                  epochs=64,
                  batch_size=60,
                  callbacks=[tensorboard_callback])

        self.__saveModel(model)

    def __createItems(self, course: list[Coordinate]) -> list[tuple[list[Coordinate], list[Command]]]:
        trajectory: list[Coordinate] = self.predictiveController.calculateTrajectory(course)

        name: str = self.coordinatesLogger.generateName('simulation')
        self.coordinatesLogger.logAsPlot(course, trajectory, name)
        self.coordinatesLogger.logAsText(trajectory, 'Trajectory', name)

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

    def __saveModel(self, model: Sequential) -> None:
        json: str = model.to_json()

        with open('model/model.json', 'w') as file:
            file.write(json)

        model.save_weights('model/model.h5')
        plot_model(model, to_file='model/model.png', show_shapes=True, show_layer_names=False)
        visualizer(model, file_name='model/graph', file_format='png')
        os.remove('model/graph')
