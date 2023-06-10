class Command:
    MOVE: int = 1
    TURN: int = 2

    def __init__(self, type: int, angle: float = None, distance: float = None) -> None:
        self.type = type
        self.angle = 0.0 if angle is None else round(angle, 2)
        self.distance = 0.0 if distance is None else round(distance, 2)

    def __eq__(self, other) -> bool:
        return self.type == other.type \
            and self.angle == other.angle \
            and self.distance == other.distance

    def __repr__(self) -> str:
        return '(' + str(self.type) + ', ' + str(self.angle) + ', ' + str(self.distance) + ')'
