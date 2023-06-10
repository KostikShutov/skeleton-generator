from keras.models import Sequential
from keras.layers import Dense, Flatten, Reshape


class PredictModel:
    def __init__(self) -> None:
        self.model = Sequential()
        self.model.add(Dense(64, activation='linear', input_shape=(2, 2)))
        self.model.add(Dense(32, activation='linear'))
        self.model.add(Flatten())
        self.model.add(Dense(2 * 3, activation='linear'))
        self.model.add(Reshape((2, 3)))
        self.model.compile(optimizer='adam', loss='mse', metrics=['mse'])

    def getModel(self) -> Sequential:
        return self.model
