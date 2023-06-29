import os


def createDirectory(directory: str) -> None:
    if not os.path.exists(directory):
        os.makedirs(directory)
