from pathlib import Path
from typing import Any

from blueapi.client.client import BlueapiClient
from blueapi.client.rest import BlueskyRemoteControlError, ServiceUnavailableError
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

    def _create_task(self, plan_name: str, plan_params: dict[str, Any]) -> TaskRequest:
        return TaskRequest(
            name=plan_name,
            params=plan_params,
            instrument_session=self.instrument_session,
        )

    def _check_instrument_session(self) -> bool:
        if not self.instrument_session:
            log_to_gui(
                LOGGER,
                "Instrument session hasn't been set, please select visit before continuing.",  # noqa: E501
                level="ERROR",
            )
            return False
        return True

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
        if self._check_instrument_session():
            task = self._create_task(plan_name, plan_params)
            try:
                self.client.create_and_start_task(task)
            except Exception as e:
                log_to_gui(
                    LOGGER,
                    f"""Something went wrong running the {plan_name} plan,
                    check out the logs for more information""",
                    level="ERROR",
                )
                LOGGER.exception(e)
        log_to_gui(LOGGER, "Run plan done", level="DEBUG")

    def run_plan_and_get_result(self, plan_name: str, plan_params: dict[str, Any]):
        if self._check_instrument_session():
            task = self._create_task(plan_name, plan_params)
            try:
                result = self.client.run_task(task)
            except ServiceUnavailableError as e:
                print("error creating task")
                LOGGER.exception(e)
            except Exception as e:
                print(f"Some other issue {e}")
                LOGGER.exception(e)
            if result.task_failed:
                print(
                    "somethign went wrong when running the plan, look at blueapi logs"
                )
            else:
                print(result.result)
        log_to_gui(LOGGER, "Run plan with result done", level="DEBUG")
