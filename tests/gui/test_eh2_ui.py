from unittest.mock import patch

import pytest
from PyQt6 import QtWidgets

from i19serial_ui.gui.grid_options import GridOptions
from i19serial_ui.gui.input_panel import InputPanel
from i19serial_ui.gui.log_box import LogBox
from i19serial_ui.gui.serial_gui_eh2 import SerialGuiEH2
from i19serial_ui.gui.wells_selection import WellsSelectionPanel


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


def test_general_layout(mock_eh2_gui):
    assert mock_eh2_gui.general_layout is not None
    assert isinstance(mock_eh2_gui.general_layout, QtWidgets.QGridLayout)
    title = mock_eh2_gui.general_layout.children()[0]
    assert isinstance(title, QtWidgets.QHBoxLayout)


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


def test_run_zebra(mock_eh2_gui):
    mock_rotation_start = 0.0
    mock_num_images = 50.0
    mock_rotation_increment = 0.2
    mock_rotation_end = mock_rotation_start + mock_num_images + mock_rotation_increment
    mock_time_image = 0.2

    mock_params = {
        "phi_start": mock_rotation_start,
        "phi_end": mock_rotation_end,
        "phi_steps": mock_num_images,
        "exposure_time": mock_time_image,
        "gate_width": mock_rotation_end - mock_rotation_start + 0.1,
        "pulse_width": mock_rotation_increment,
    }
    mock_eh2_gui.test_btn1.click()
    mock_eh2_gui.client.run_plan.assert_called_once_with("run_zebra_test", mock_params)


def test_run_panda(mock_eh2_gui):
    mock_rotation_start = 0.0
    mock_num_images = 50.0
    mock_rotation_increment = 0.2
    mock_rotation_end = mock_rotation_start + mock_num_images + mock_rotation_increment
    mock_time_image = 0.2
    mock_params = {
        "phi_start": mock_rotation_start,
        "phi_end": mock_rotation_end,
        "phi_steps": mock_num_images,
        "exposure_time": mock_time_image,
    }
    mock_eh2_gui.test_btn2.click()
    mock_eh2_gui.client.run_plan.assert_called_once_with("run_panda_test", mock_params)
