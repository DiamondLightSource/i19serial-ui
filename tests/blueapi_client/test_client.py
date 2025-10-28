from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from blueapi.client.client import BlueapiClient
from blueapi.config import ApplicationConfig

from i19serial_ui.blueapi_tools.blueapi_client import SerialBlueapiClient


@pytest.fixture
def mock_client() -> SerialBlueapiClient:
    with patch(
        "i19serial_ui.blueapi_tools.blueapi_client.SerialBlueapiClient._load_config_from_file"
    ) as patch_config:
        patch_config.return_value = ApplicationConfig()
        client = SerialBlueapiClient(Path("/some/config.yaml"))
    return client


def test_client_started(mock_client: SerialBlueapiClient):
    assert mock_client.client and isinstance(mock_client.client, BlueapiClient)


@patch("i19serial_ui.blueapi_tools.blueapi_client.LOGGER")
@patch("i19serial_ui.blueapi_tools.blueapi_client.log_to_gui")
def test_run_plan_exits_with_error_message_if_no_instrument_session(
    patch_log: MagicMock, patch_logger: MagicMock, mock_client: SerialBlueapiClient
):
    mock_client.run_plan("some_plan", {})

    patch_log.assert_called_once_with(
        patch_logger,
        "Instrument session hasn't been set, please select visit before continuing.",
        level="ERROR",
    )


@patch("i19serial_ui.blueapi_tools.blueapi_client.log_to_gui")
def test_client_update_session(patch_log: MagicMock, mock_client: SerialBlueapiClient):
    assert not mock_client.instrument_session

    mock_client.update_session("cm12345-1")
    assert mock_client.instrument_session == "cm12345-1"
    patch_log.assert_called_once()


def test_run_plan(mock_client: SerialBlueapiClient):
    mock_client.client = MagicMock(spec=BlueapiClient)

    mock_client.update_session("cm12345-1")
    mock_client.run_plan("some_plan", {"param": 1})

    mock_client.client.create_and_start_task.assert_called_once()
