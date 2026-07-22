from collections import deque
from unittest.mock import call, patch

import pytest

from i19serial_ui.blueapi_tools.blueapi_queue import BlueapiQueueRunner
from i19serial_ui.parameters.queue import QueueElement


@pytest.fixture
def mock_queue():
    return deque(
        [
            QueueElement("serial_plan_1", {"dataset": "a"}),
            QueueElement("serial_plan_2", {"dataset": "b"}),
        ]
    )


@pytest.fixture
def mock_queue_runner(mock_queue) -> BlueapiQueueRunner:
    with patch(
        "i19serial_ui.blueapi_tools.blueapi_queue.SerialBlueapiClient"
    ) as mock_client:
        test_queue = BlueapiQueueRunner(mock_client, mock_queue)
        return test_queue


def test_start_queue(mock_queue_runner):
    mock_queue_runner._client.get_worker_state.return_value = "IDLE"
    mock_queue_runner.start()

    assert mock_queue_runner._client.run_plan.call_count == 2
    mock_queue_runner._client.run_plan.assert_has_calls(
        [
            call("serial_plan_1", {"parameters": {"dataset": "a"}}),
            call("serial_plan_2", {"parameters": {"dataset": "b"}}),
        ]
    )
