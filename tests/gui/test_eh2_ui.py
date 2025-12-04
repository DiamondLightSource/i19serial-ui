from unittest.mock import patch

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
