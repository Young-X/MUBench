from typing import List

from nose.tools import assert_is_instance, assert_raises

from tasks.configurations.configurations import TaskConfiguration, get_task_configuration
from tasks.configurations.mubench_paths import MubenchPaths


class ConfigDummy:
    def __init__(self, mode: str):
        self.task = mode
        self.publish_task = ""


class TestTaskConfigurations:
    def test_get_configuration(self):
        configuration = get_task_configuration(MubenchPaths, ConfigDummy("-test-"))
        assert_is_instance(configuration, TaskConfigurationTestImpl)

    def test_duplicate_raises_value_error(self):
        assert_raises(ValueError, get_task_configuration, MubenchPaths, ConfigDummy("-duplicate-"))

    def test_no_available_configuration_raises_value_error(self):
        assert_raises(ValueError, get_task_configuration, MubenchPaths, ConfigDummy("-unavailable-"))


class TaskConfigurationTestImpl(TaskConfiguration):
    @staticmethod
    def mode() -> str:
        return "-test-"

    def _tasks(self, paths: MubenchPaths, config) -> List:
        return []


class DuplicateTaskConfiguration(TaskConfiguration):
    def _tasks(self, paths: MubenchPaths, config) -> List:
        return []

    @staticmethod
    def mode() -> str:
        return "-duplicate-"


class DuplicateTaskConfiguration2(TaskConfiguration):
    def _tasks(self, paths: MubenchPaths, config) -> List:
        return []

    @staticmethod
    def mode() -> str:
        return "-duplicate-"
