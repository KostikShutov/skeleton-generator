import os
import json
import logging
import tensorflow as tf
from datetime import datetime
from collections.abc import Iterable
from keras.models import Sequential
from keras.utils import plot_model
from keras_visualizer import visualizer
from common.commands.Command import Command
from common.commands.CommandsService import CommandsService
from common.coordinates.Coordinate import Coordinate
from common.coordinates.CoordinatesParser import CoordinatesParser
from common.coordinates.CoordinatesService import CoordinatesService
from predictor.PredictModel import PredictModel
from trainer.CommandsCreator import CommandsCreator


class TrainService:
    def __init__(self, coordinatesParser: CoordinatesParser,
                 coordinatesService: CoordinatesService,
                 commandsCreator: CommandsCreator,
                 commandsService: CommandsService) -> None:
        self.coordinatesParser = coordinatesParser
        self.coordinatesService = coordinatesService
        self.commandsCreator = commandsCreator
        self.commandsService = commandsService

    def train(self) -> None:
        with open('model/train.json', 'r') as file:
            data: Iterable = json.load(file)

        model: Sequential = PredictModel().getModel()
        trainX: list[list[float]] = []
        trainY: list[list[float, float]] = []

        for i, item in enumerate(data):
            course: list[Coordinate] = self.coordinatesParser.parse(item)
            commands: list[tuple[list[Coordinate], Command]] = self.commandsCreator.create(course)

            for part, command in commands:
                flattenX: list[float] = self.coordinatesService.flattenWithRound(part)
                flattenY: list[float, float] = self.commandsService.flattenWithRound(command)

                logging.debug('Train input part: %s' % flattenX)
                logging.debug('Train target part: %s' % flattenY)

                trainX.append(flattenX)
                trainY.append(flattenY)

        tensorboard_dir: str = 'logs/tensorboard/' + datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=tensorboard_dir, histogram_freq=1)

        model.fit(x=trainX,
                  y=trainY,
                  epochs=64,
                  batch_size=60,
                  callbacks=[tensorboard_callback])

        self.__saveModel(model)

    def __saveModel(self, model: Sequential) -> None:
        json: str = model.to_json()

        with open('model/model.json', 'w') as file:
            file.write(json)

        model.save_weights('model/model.h5')
        plot_model(model, to_file='model/model.png', show_shapes=True, show_layer_names=False)
        visualizer(model, file_name='model/graph', file_format='png')
        os.remove('model/graph')
