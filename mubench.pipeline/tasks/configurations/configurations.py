from typing import List



class TaskConfiguration(list):
    def __init__(self, paths: MubenchPaths, config):
        super().__init__()
        self.extend(self._tasks(paths, config))

    @staticmethod
    def mode() -> str:
        raise NotImplementedError

    def _tasks(self, paths: MubenchPaths, config) -> List:
        raise NotImplementedError


def get_task_configuration(paths: MubenchPaths, config) -> TaskConfiguration:
    mode = config.task
    if config.publish_task:
        mode += " " + config.publish_task

    requested_configurations = [task_config(paths, config) for task_config in
                                TaskConfiguration.__subclasses__() if task_config.mode() == mode]
    if len(requested_configurations) > 1:
        raise ValueError("Multiple configurations for {}".format(mode))
    if len(requested_configurations) == 0:
        raise ValueError("No configuration available for {}".format(mode))

    return requested_configurations[0]
