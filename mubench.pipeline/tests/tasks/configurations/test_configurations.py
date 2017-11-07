from typing import List

from nose.tools import assert_is_instance, assert_raises

from tasks.configurations.configurations import Configuration, get_configuration


class TestConfigurations:
    def test_get_configuration(self):
        configuration = get_configuration("-test-")
        assert_is_instance(configuration, ConfigurationTestImpl)

    def test_duplicate_raises_value_error(self):
        assert_raises(ValueError, get_configuration, "-duplicate-")

    def test_no_available_configuration_raises_value_error(self):
        assert_raises(ValueError, get_configuration, "-unavailable-")


class ConfigurationTestImpl(Configuration):
    def mode(self) -> str:
        return "-test-"

    def _tasks(self) -> List:
        return []


class DuplicateConfiguration(Configuration):
    def _tasks(self) -> List:
        return []

    def mode(self) -> str:
        return "-duplicate-"


class DuplicateConfiguration2(Configuration):
    def _tasks(self) -> List:
        return []

    def mode(self) -> str:
        return "-duplicate-"
