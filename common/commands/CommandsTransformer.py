from common.commands.Command import Command


class CommandsTransformer:
    def flatten(self, commands: list[Command]) -> list[list[int, float, float]]:
        flattened: list[list[int, float, float]] = []

        for command in commands:
            flattened.append([command.type, command.angle, command.distance])

        return flattened
