import logging

import pytest
from PyQt6 import QtWidgets

from i19serial_ui.gui.widgets.log_box import GREETING, LogBox
from i19serial_ui.log import GuiWindowLogHandler


@pytest.fixture
def mock_gui_handler():
    return GuiWindowLogHandler()


@pytest.fixture
def mock_log_box(mock_gui_handler, qtbot):
    test_box = LogBox(QtWidgets.QWidget(), mock_gui_handler)
    qtbot.addWidget(test_box)
    return test_box


def test_start_up_greeting_in_log_box(mock_log_box):
    assert mock_log_box.log_output_box.toPlainText() == GREETING


def test_log_box_updated_with_log_message(mock_log_box, mock_gui_handler):
    log_record = logging.LogRecord(
        "Info", logging.INFO, "", 0, "Hello test", None, None
    )
    mock_gui_handler.emit(log_record)
    full_log = mock_log_box.log_output_box.toPlainText()
    assert full_log.split("\n")[-1] == "Hello test"
