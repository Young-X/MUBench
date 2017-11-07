from typing import List


class Configuration(list):
    def __init__(self):
        super().__init__()
        self.extend(self._tasks())

    def mode(self) -> str:
        raise NotImplementedError

    def _tasks(self) -> List:
        raise NotImplementedError


def get_configuration(mode: str) -> Configuration:
    requested_configurations = [conf() for conf in Configuration.__subclasses__() if conf().mode() == mode]
    if len(requested_configurations) > 1:
        raise ValueError("Multiple configurations for mode {}".format(mode))
    if len(requested_configurations) == 0:
        raise ValueError("No configuration available for mode {}".format(mode))

    return requested_configurations[0]
