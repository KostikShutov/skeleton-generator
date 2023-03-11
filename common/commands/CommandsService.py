from common.commands.Command import Command


class CommandsService:
    def flattenWithRound(self, command: Command) -> list[float]:
        return [round(command.angle, 2), round(command.distance, 2)]
