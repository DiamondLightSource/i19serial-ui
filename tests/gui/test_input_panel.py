import pytest
from PyQt6 import QtWidgets

from i19serial_ui.gui.input_panel import InputPanel


@pytest.fixture
def mock_input_panel(qtbot):
    test_panel = InputPanel()
    qtbot.addWidget(test_panel)
    return test_panel


def test_input_boxes_created_with_defaults(mock_input_panel):
    assert isinstance(mock_input_panel.inputs_layout, QtWidgets.QGridLayout)
    expected_defaults = [
        (mock_input_panel.num_images, "50"),
        (mock_input_panel.time_image, "0.2"),
        (mock_input_panel.image_width, "0.2"),
        (mock_input_panel.det_dist, "117.53"),
        (mock_input_panel.transmission, "5"),
        (mock_input_panel.well_start, "1"),
        (mock_input_panel.well_end, "10"),
        (mock_input_panel.series_length, "1"),
        (mock_input_panel.two_theta, "0"),
    ]

    for text_box, default_value in expected_defaults:
        assert text_box.text() == default_value


def test_input_boxes_can_be_updated(mock_input_panel):
    updated = [
        (mock_input_panel.num_images, "20"),
        (mock_input_panel.time_image, "0.1"),
        (mock_input_panel.image_width, "5"),
        (mock_input_panel.det_dist, "2"),
        (mock_input_panel.transmission, "6"),
        (mock_input_panel.well_start, "2"),
        (mock_input_panel.well_end, "40"),
        (mock_input_panel.series_length, "3"),
        (mock_input_panel.two_theta, "2"),
    ]

    for text_box, updated_value in updated:
        text_box.setText(updated_value)
        assert text_box.text() == updated_value
