from collections import deque

import pytest

from i19serial_ui.gui.widgets.queue.queue_table import QueueTable
from i19serial_ui.parameters.queue import QueueElement

queue_elements = [
    QueueElement(
        plan_name="collection_plan",
        plan_params={"dataset": "test1", "exposure_time_s": 0.1},
    ),
    QueueElement(
        plan_name="collection_plan",
        plan_params={"dataset": "test2", "exposure_time_s": 0.1},
    ),
]


@pytest.fixture
def mock_queue_table(qtbot):
    test_table = QueueTable(queue=deque())
    qtbot.addWidget(test_table)
    return test_table


def test_queue_table(mock_queue_table):
    assert mock_queue_table.rowCount() == 0
    assert mock_queue_table.columnCount() == 3


def test_queue_table_add_row(mock_queue_table):
    # Simulate what happens upstream by adding to queue
    mock_queue_table.queue.append(queue_elements[0])
    mock_queue_table.add_row(queue_elements[0])

    assert mock_queue_table.rowCount() == 1

    # Simulate what happens upstream by adding to queue
    mock_queue_table.queue.append(queue_elements[1])
    mock_queue_table.add_row(queue_elements[1])

    assert mock_queue_table.rowCount() == 2


def test_queue_table_remove_row_signal_emitted(mock_queue_table, qtbot):
    mock_queue_table.queue.append(queue_elements[0])
    with qtbot.waitSignal(mock_queue_table.remove_item_request) as sig:
        mock_queue_table.delete_row(queue_elements[0])

        assert sig.args[0] == queue_elements[0]
