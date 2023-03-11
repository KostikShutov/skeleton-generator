from keras.models import Sequential
from keras.layers import Dense


class InterpolateModel:
    def __init__(self) -> None:
        self.model = Sequential()
        self.model.add(Dense(8, input_dim=1, activation='relu'))
        self.model.add(Dense(64, activation='relu'))
        self.model.add(Dense(64, activation='relu'))
        self.model.add(Dense(1, activation='linear'))
        self.model.compile(optimizer='adam', loss='mse', metrics=['mse'])

    def getModel(self) -> Sequential:
        return self.model
