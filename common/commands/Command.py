class Command:
    def __init__(self, angle: float, distance: float) -> None:
        self.angle = angle
        self.distance = distance

    def __eq__(self, other) -> bool:
        return self.angle == other.angle and self.distance == other.distance

    def __repr__(self):
        return '(' + str(self.angle) + ', ' + str(self.distance) + ')'
