import pytest
import os
import json

from kaa.kaa_definition import DefinitionException, KaaDefinition


class TestKaaDefinition:
    base_path = os.path.dirname(__file__)

    def test_bad_data(self):
        with pytest.raises(DefinitionException):
            KaaDefinition(self.__get_json_path("unknown.json"))

        with pytest.raises(DefinitionException):
            KaaDefinition(self.__get_json_path("bad.json"))

        with pytest.raises(DefinitionException):
            KaaDefinition(self.__get_json_path("server_missing.json"))

    def test_default_values(self):
        definition = DefinitionDefaults(self.__get_json_path("default_values.json"))
        assert KaaDefinition.DEFAULT_NAME == definition.get_name()
        assert KaaDefinition.DEFAULT_VERSION == definition.get_version()
        assert KaaDefinition.DEFAULT_BASE_PATH == definition.get_base_path()
        assert KaaDefinition.DEFAULT_DEBUG == definition.is_debug()
        assert KaaDefinition.DEFAULT_ENABLE_CORS == definition.cors_enabled()
        assert KaaDefinition.DEFAULT_POLLING_ENABLED == definition.is_polling_enabled()
        assert KaaDefinition.DEFAULT_POLLING_INTERVAL, definition.get_polling_interval()
        assert (
            KaaDefinition.DEFAULT_POLLING_INCLUDE_DIRS,
            KaaDefinition.DEFAULT_POLLING_INCLUDE_FILES,
        ) == definition.get_polling_inclusions()
        assert (
            KaaDefinition.DEFAULT_POLLING_EXCLUDE_DIRS,
            KaaDefinition.DEFAULT_POLLING_EXCLUDE_FILES,
        ) == definition.get_polling_exclusions()

    def test_with_values(self):
        json_path = self.__get_json_path("with_values.json")
        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        definition_value = DefinitionsWithValues(json_path)
        assert data["name"] == definition_value.get_name()
        assert data["server"] == definition_value.get_server()
        assert data["version"] == definition_value.get_version()
        assert data["debug"] == definition_value.is_debug()
        assert data["enableCors"] == definition_value.cors_enabled()

        polling = data["developmentPolling"]
        assert polling["enabled"] == definition_value.is_polling_enabled()
        assert polling["intervalSeconds"] == definition_value.get_polling_interval()

        inclusions = polling["inclusions"]
        assert (
            inclusions["directories"],
            inclusions["files"],
        ) == definition_value.get_polling_inclusions()

        exclusions = polling["exclusions"]
        assert (
            exclusions["directories"],
            exclusions["files"],
        ) == definition_value.get_polling_exclusions()

    def __get_json_path(self, file_name):
        return f"{self.base_path}/fixtures/{file_name}"


class DefinitionDefaults(KaaDefinition):
    pass


class DefinitionsWithValues(KaaDefinition):
    pass
