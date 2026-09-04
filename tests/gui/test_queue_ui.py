import pytest
from PyQt6 import QtWidgets

from i19serial_ui.gui.widgets.queue.queue_table import QueueTable
from i19serial_ui.gui.widgets.queue.queue_ui import RunQueueUI
from i19serial_ui.parameters.queue import QueueElement

QUEUE = [
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
def mock_queue_ui(qtbot):
    queue_ui = RunQueueUI()
    qtbot.addWidget(queue_ui)
    return queue_ui


def test_run_queue_ui(mock_queue_ui):
    # Starting window
    assert len(mock_queue_ui.run_queue) == 0
    assert mock_queue_ui.visit_txt.text() == ""

    assert isinstance(mock_queue_ui.table, QueueTable)
    assert mock_queue_ui.layout().count() == 2

    assert isinstance(mock_queue_ui.layout(), QtWidgets.QVBoxLayout)

    visit_layout = mock_queue_ui.layout().children()[0]
    assert isinstance(visit_layout, QtWidgets.QHBoxLayout)


def test_add_item_to_queue(mock_queue_ui):
    new_item = QUEUE[0]

    mock_queue_ui.add_to_queue_table(new_item)

    assert len(mock_queue_ui.run_queue) == 1
    assert mock_queue_ui.table.rowCount() == 1

    btn = mock_queue_ui.table.cellWidget(0, 0)
    assert isinstance(btn, QtWidgets.QPushButton)
    assert mock_queue_ui.table.item(0, 1).text() == new_item.element_label
    assert mock_queue_ui.table.item(0, 2).text() == str(new_item.plan_params)


def test_clear_queue_table(mock_queue_ui):
    for item in QUEUE:
        mock_queue_ui.add_to_queue_table(item)

    assert mock_queue_ui.table.rowCount() == 2
    assert len(mock_queue_ui.run_queue) == 2

    mock_queue_ui.clear_queue_table()

    assert mock_queue_ui.table.rowCount() == 0
    assert len(mock_queue_ui.run_queue) == 0


def test_on_delete_click(mock_queue_ui):
    for item in QUEUE:
        mock_queue_ui.add_to_queue_table(item)

    # Get btn of first row and click
    delete_btn_1 = mock_queue_ui.table.cellWidget(0, 0)

    delete_btn_1.click()  # type:ignore

    assert mock_queue_ui.table.rowCount() == 1
    assert len(mock_queue_ui.run_queue) == 1
