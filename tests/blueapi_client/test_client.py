from pathlib import Path
from unittest.mock import MagicMock, call, patch

import pytest
from blueapi.client.client import BlueapiClient

# from blueapi.client.rest import ServiceUnavailableError
from blueapi.config import ApplicationConfig
from blueapi.service.model import TaskRequest
from blueapi.worker.event import TaskResult, TaskStatus

from i19serial_ui.blueapi_tools.blueapi_client import (
    SerialBlueapiClient,
    WrongConfigFileFormatError,
)


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

    expected_log_calls = [
        call(
            patch_logger,
            "Instrument session hasn't been set, please select visit before continuing.",  # noqa: E501
            level="ERROR",
        ),
        call(
            patch_logger,
            "Run plan done",
            level="DEBUG",
        ),
    ]

    patch_log.assert_has_calls(expected_log_calls)


@pytest.mark.parametrize("session, expected_result", [("", False), ("cm12345-1", True)])
def test_check_instrument_session(
    session: str,
    expected_result: bool,
    mock_client: SerialBlueapiClient,
):
    mock_client.update_session(session)
    check_result = mock_client._check_instrument_session()

    assert check_result is expected_result


@patch("i19serial_ui.blueapi_tools.blueapi_client.log_to_gui")
def test_client_update_session(patch_log: MagicMock, mock_client: SerialBlueapiClient):
    assert not mock_client.instrument_session

    mock_client.update_session("cm12345-1")
    assert mock_client.instrument_session == "cm12345-1"
    patch_log.assert_called_once()


def test_client_create_task(mock_client: SerialBlueapiClient):
    mock_client.update_session("cm12345-1")
    task = mock_client._create_task("new_plan", {"x": 10})

    assert isinstance(task, TaskRequest)
    assert task.name == "new_plan"
    assert task.params == {"x": 10}
    assert task.instrument_session == "cm12345-1"


def test_run_plan(mock_client: SerialBlueapiClient):
    mock_client.client = MagicMock(spec=BlueapiClient)

    mock_client.update_session("cm12345-1")
    mock_client.run_plan("some_plan", {"param": 1})

    mock_client.client.create_and_start_task.assert_called_once()


def test_client_error_if_config_file_not_yaml():
    with pytest.raises(WrongConfigFileFormatError):
        SerialBlueapiClient(Path("some_file.csv"))


@pytest.mark.parametrize(
    "failure, result, expected_result", [(False, "Hello", "Hello"), (True, "", None)]
)
def test_run_plan_and_get_its_result(
    failure: bool,
    result: str,
    expected_result: str | None,
    mock_client: SerialBlueapiClient,
):
    mock_client.client = MagicMock(spec=BlueapiClient)
    mock_client.client.run_task.return_value = TaskStatus(
        task_id="abcd",
        result=TaskResult(outcome="success", result=result, type="string"),
        task_complete=True,
        task_failed=failure,
    )

    mock_client.update_session("cm12345-1")
    res = mock_client.run_plan_and_get_result("some_plan", {"param": 1})

    mock_client.client.run_task.assert_called_once_with(
        TaskRequest(
            name="some_plan", params={"param": 1}, instrument_session="cm12345-1"
        )
    )

    assert res == expected_result
