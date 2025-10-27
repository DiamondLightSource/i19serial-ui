import pytest
from PyQt6 import QtWidgets

from i19serial_ui.gui.grid_options import GridOptions
from i19serial_ui.gui.input_panel import InputPanel
from i19serial_ui.gui.log_box import LogBox
from i19serial_ui.gui.serial_gui_eh2 import SerialGuiEH2
from i19serial_ui.gui.wells_selection import WellsSelectionPanel


@pytest.fixture
def mock_eh2_gui(qtbot):
    test_gui = SerialGuiEH2()
    qtbot.addWidget(test_gui)
    return test_gui


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
