import pytest
from PyQt6 import QtWidgets

from i19serial_ui.gui.input_panel import InputPanel


@pytest.fixture
def mock_input_panel(qtbot):
    test_panel = InputPanel()
    qtbot.addWidget(test_panel)
    return test_panel


def test_input_boxes_created_with_defaults(mock_input_panel):
    assert isinstance(mock_input_panel.inputs_layout, QtWidgets.QHBoxLayout)
    assert mock_input_panel.num_images.text() == "1"
    assert mock_input_panel.time_image.text() == "0.2"


def test_input_boxes_can_be_updated(mock_input_panel):
    mock_input_panel.num_images.setText("20")
    mock_input_panel.time_image.setText("0.1")

    assert mock_input_panel.num_images.text() == "20"
    assert mock_input_panel.time_image.text() == "0.1"
