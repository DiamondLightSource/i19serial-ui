import pytest
from PyQt6 import QtWidgets

from i19serial_ui.gui.input_panel import InputPanel


@pytest.fixture
def mock_input_panel(qtbot):
    test_panel = InputPanel()
    test_panel.visit_path.setText("/path/to/visit")
    qtbot.addWidget(test_panel)
    return test_panel


def test_all_layouts_added_to_input_panel(mock_input_panel):
    assert mock_input_panel.inputs_layout is not None
    assert isinstance(mock_input_panel.inputs_layout, QtWidgets.QVBoxLayout)
    assert mock_input_panel.inputs_layout.count() == 3  # Number of chidren


def test_visit_box_is_read_only(mock_input_panel):
    assert mock_input_panel.visit_path.isReadOnly()
    assert mock_input_panel.visit_path.text() == "/path/to/visit"


def test_input_dataset_created_and_can_be_updated(mock_input_panel):
    assert isinstance(
        mock_input_panel.inputs_layout.children()[1], QtWidgets.QHBoxLayout
    )

    assert mock_input_panel.dataset.text() == ""
    assert mock_input_panel.prefix.text() == ""

    mock_input_panel.dataset.setText("foo/")
    mock_input_panel.prefix.setText("bar")

    assert mock_input_panel.dataset.text() == "foo/"
    assert mock_input_panel.prefix.text() == "bar"


def test_input_params_boxes_created_with_defaults(mock_input_panel):
    assert isinstance(
        mock_input_panel.inputs_layout.children()[2], QtWidgets.QGridLayout
    )
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
        (mock_input_panel.rotation_start, "0"),
    ]

    for text_box, default_value in expected_defaults:
        assert text_box.text() == default_value


def test_input_params_boxes_can_be_updated(mock_input_panel):
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
        (mock_input_panel.rotation_start, "5"),
    ]

    for text_box, updated_value in updated:
        text_box.setText(updated_value)
        assert text_box.text() == updated_value
