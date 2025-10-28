from pathlib import Path

from blueapi.client.client import BlueapiClient
from blueapi.config import ApplicationConfig, ConfigLoader


class SerialBlueapiClient:
    def __init__(self, config_file: Path, session: str = ""):
        self.instrument_session = session
        self.client = self._get_blueapi_client(config_file)

    def _get_blueapi_client(self, config_file) -> BlueapiClient:
        config_loader = ConfigLoader(ApplicationConfig)
        config_loader.use_values_from_yaml(config_file)
        config = config_loader.load()
        return BlueapiClient.from_config(config)

    def update_session(self, new_session: str):
        self.instrument_session = new_session
