import pytest

from i19serial_ui.gui.widgets.queue.queue_table import QueueTable
from i19serial_ui.parameters.queue import QueueElement


@pytest.fixture
def mock_queue_table(qtbot):
    test_table = QueueTable()
    qtbot.addWidget(test_table)
    return test_table


def test_queue_table(mock_queue_table):
    assert mock_queue_table.rowCount() == 0
    assert mock_queue_table.columnCount() == 3


def test_fill_in_table(mock_queue_table):
    new_item = QueueElement(
        plan_name="collection_plan",
        plan_params={"dataset": "test1", "exposure_time_s": 0.1},
    )
    mock_queue_table.insertRow(0)
    mock_queue_table.fill_in_table(new_item, 0)

    assert mock_queue_table.rowCount() == 1

    assert mock_queue_table.item(0, 1).text() == new_item.element_label
    assert mock_queue_table.item(0, 2).text() == str(new_item.plan_params)


def test_clear_finished_task_removes_row(mock_queue_table):
    for i in range(3):
        mock_queue_table.insertRow(i)

    assert mock_queue_table.rowCount() == 3

    mock_queue_table.clear_finished_task(1)
    assert mock_queue_table.rowCount() == 2
