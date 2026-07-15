import pytest
from PyQt6 import QtWidgets

from i19serial_ui.gui.widgets.queue.queue_table import QueueTable
from i19serial_ui.gui.widgets.queue.queue_ui import RunQueueUI
from i19serial_ui.parameters.queue import QueueElement


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
    new_item = QueueElement(
        plan_name="collection_plan",
        plan_params={"dataset": "test1", "exposure_time_s": 0.1},
    )

    mock_queue_ui.add_to_queue_table(new_item)

    assert len(mock_queue_ui.run_queue) == 1
    assert len(mock_queue_ui.table.queue) == 1
    assert mock_queue_ui.table.rowCount() == 1
