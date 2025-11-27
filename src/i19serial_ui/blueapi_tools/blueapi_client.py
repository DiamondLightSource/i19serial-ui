from pathlib import Path
from typing import Any

from blueapi.client.client import BlueapiClient
from blueapi.client.rest import BlueskyRemoteControlError
from blueapi.config import ApplicationConfig, ConfigLoader
from blueapi.service.model import TaskRequest

from i19serial_ui.log import LOGGER, log_to_gui


class WrongConfigFileFormatError(Exception):
    pass


class SerialBlueapiClient:
    def __init__(self, config_file: Path, session: str = ""):
        # TODO Needs a callback for logging reasons, probably
        # See https://github.com/DiamondLightSource/i19serial-ui/issues/22
        self.instrument_session = session
        self.client = self._get_blueapi_client(config_file)

    def _load_config_from_file(self, config_file) -> ApplicationConfig:
        config_loader = ConfigLoader(ApplicationConfig)
        if config_file.suffix != ".yaml":
            raise WrongConfigFileFormatError(
                """The config file passed for Blueapi is not a yaml file.
                Impossible to start up the client."""
            )
        config_loader.use_values_from_yaml(config_file)
        return config_loader.load()

    def _get_blueapi_client(self, config_file) -> BlueapiClient:
        config = self._load_config_from_file(config_file)
        return BlueapiClient.from_config(config)

    def update_session(self, new_session: str):
        self.instrument_session = new_session
        log_to_gui(LOGGER, f"Session updated: {self.instrument_session}")

    def abort_task(self):
        try:
            self.client.abort()
        except BlueskyRemoteControlError:
            # TO avoid GUI dying on double clicks
            log_to_gui(LOGGER, "Abort: Nothing seems to be running.")

    def run_plan(self, plan_name: str, plan_params: dict[str, Any]):
        if not self.instrument_session:
            log_to_gui(
                LOGGER,
                "Instrument session hasn't been set, please select visit before continuing.",  # noqa: E501
                level="ERROR",
            )
            return
        task = TaskRequest(
            name=plan_name,
            params=plan_params,
            instrument_session=self.instrument_session,
        )
        self.client.create_and_start_task(task)
