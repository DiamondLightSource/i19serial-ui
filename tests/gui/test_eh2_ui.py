from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from PyQt6 import QtWidgets

from i19serial_ui.gui.serial_gui_eh2 import SerialGuiEH2
from i19serial_ui.gui.widgets import (
    GridOptions,
    InputPanel,
    LogBox,
    WellsSelectionPanel,
)


@pytest.fixture
def mock_eh2_gui(qtbot):
    with patch("i19serial_ui.gui.serial_gui_eh2.SerialBlueapiClient"):
        test_gui = SerialGuiEH2()
        qtbot.addWidget(test_gui)
        return test_gui


def test_correct_hutch_set(mock_eh2_gui):
    assert mock_eh2_gui.hutch == "EH2"


def test_all_widgets_initialised(mock_eh2_gui):
    assert mock_eh2_gui.log_widget and isinstance(mock_eh2_gui.log_widget, LogBox)
    assert mock_eh2_gui.inputs and isinstance(mock_eh2_gui.inputs, InputPanel)
    assert mock_eh2_gui.wells and isinstance(mock_eh2_gui.wells, WellsSelectionPanel)
    assert mock_eh2_gui.grid and isinstance(mock_eh2_gui.grid, GridOptions)
    assert mock_eh2_gui.aperturedropdown and isinstance(
        mock_eh2_gui.aperturedropdown, QtWidgets.QComboBox
    )


def test_general_layout(mock_eh2_gui):
    assert mock_eh2_gui.general_layout is not None
    assert isinstance(mock_eh2_gui.general_layout, QtWidgets.QGridLayout)
    title = mock_eh2_gui.general_layout.children()[0]
    assert isinstance(title, QtWidgets.QHBoxLayout)
    assert isinstance(mock_eh2_gui.top_group, QtWidgets.QGroupBox)


@pytest.mark.parametrize(
    "aperture,index", [("20um", 0), ("40um", 1), ("100um", 2), ("3000um", 3)]
)
def test_dropdown_update(mock_eh2_gui, aperture, index):
    mock_eh2_gui.aperturedropdown.setCurrentIndex(index)
    assert mock_eh2_gui.read_aperture_dropdown() == aperture


def test_select_visit(mock_eh2_gui):
    with patch(
        "i19serial_ui.gui.serial_gui_eh2.QtWidgets.QFileDialog.getExistingDirectory"
    ) as patch_dir:
        patch_dir.return_value = "/path/to/data/cm12345-1"
        mock_eh2_gui.select_visit_action.trigger()

        assert mock_eh2_gui.inputs.visit_path.text() == "/path/to/data/cm12345-1"
        mock_eh2_gui.client.update_session.assert_called_once_with("cm12345-1")


def test_abort_button(mock_eh2_gui):
    mock_eh2_gui.abort_btn.click()
    mock_eh2_gui.client.abort_task.assert_called_once()


def make_text_mock(value):
    m = Mock()
    m.text.return_value = str(value)
    return m


@pytest.mark.parametrize(
    "well_list,manual_selection_enabled,series_length",
    [([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], False, 1), ([1, 3, 5, 7, 9], True, 2)],
)
def test_run_panda_and_read_all_parameters(
    # mock_read_wells: MagicMock,
    mock_eh2_gui,
    well_list,
    manual_selection_enabled,
    series_length,
):
    mock_detector_z = 117.53
    mock_eh2_aperture = "20um"  # ApertureOptions.UM_20
    mock_detector_two_theta = 0.0
    mock_rotation_start = 0.0
    mock_num_images = 50.0
    mock_rotation_increment = 0.2
    mock_rotation_end = mock_rotation_start + mock_num_images + mock_rotation_increment
    mock_time_image = 0.2

    inputs = mock_eh2_gui.inputs

    inputs.rotation_start = make_text_mock(mock_rotation_start)
    inputs.num_images = make_text_mock(mock_num_images)
    inputs.image_width = make_text_mock(mock_rotation_increment)

    inputs.det_dist = make_text_mock(mock_detector_z)
    inputs.two_theta = make_text_mock(mock_detector_two_theta)
    inputs.time_image = make_text_mock(mock_time_image)

    inputs.series_length = make_text_mock(series_length)

    inputs.visit_path = make_text_mock(".")
    inputs.dataset = make_text_mock("")
    inputs.prefix = make_text_mock("")
    inputs.transmission = make_text_mock(5.0)

    inputs.well_start = make_text_mock(well_list[0])
    inputs.well_end = make_text_mock(well_list[-1])

    mock_eh2_gui.grid.grid_box.currentText = Mock(return_value="polymer")
    mock_eh2_gui.grid.grid_x = make_text_mock(20)
    mock_eh2_gui.grid.grid_z = make_text_mock(20)

    mock_eh2_gui.read_aperture_dropdown = Mock(return_value=mock_eh2_aperture)

    mock_eh2_gui.wells.selection_checkbox.isChecked = Mock(
        return_value=manual_selection_enabled
    )
    mock_eh2_gui.wells.get_selected_wells_list = Mock(return_value=well_list)
    mock_params = {
        "parameters": {
            "detector_distance_mm": mock_detector_z,
            "two_theta_deg": mock_detector_two_theta,
            "rot_axis_start": mock_rotation_start,
            "rot_axis_end": mock_rotation_end,
            "rot_axis_increment": 0.2,
            "images_per_well": mock_num_images,
            "exposure_time_s": mock_time_image,
            "aperture_request": mock_eh2_aperture,
            "hutch": "EH2",
            "visit": Path("."),
            "dataset": "",
            "filename_prefix": "",
            "image_width_deg": 0.2,
            "transmission_fraction": 5.0,
            "grid": {
                "grid_type": "polymer",
                "x_steps": 20,
                "z_steps": 20,
            },
            "detector_type": "EIGER",
            "well_position": {1: (1, 2, 3)},
            "wells": mock_eh2_gui.read_wells(),
        }
    }
    mock_eh2_gui.run_btn.click()
    mock_eh2_gui.client.run_plan.assert_called_once_with(
        "run_serial_from_panda", mock_params
    )
