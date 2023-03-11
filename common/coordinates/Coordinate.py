class Coordinate:
    def __init__(self, x: float, y: float, angle: float = 0.0) -> None:
        self.x = x
        self.y = y
        self.angle = angle

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y and self.angle == other.angle

    def __repr__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ', ' + str(self.angle) + ')'
