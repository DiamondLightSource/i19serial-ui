import pytest
from PyQt6 import QtWidgets

from i19serial_ui.gui.wells_selection import WellsSelectionPanel


@pytest.fixture
def mock_wells_panel(qtbot):
    test_panel = WellsSelectionPanel()
    qtbot.addWidget(test_panel)
    return test_panel


def test_wells_selection_panel(mock_wells_panel):
    assert mock_wells_panel.selection_layout is not None
    assert isinstance(mock_wells_panel.selection_layout, QtWidgets.QHBoxLayout)


def test_selection_checkbox(mock_wells_panel):
    assert not mock_wells_panel.selection_checkbox.isChecked()

    mock_wells_panel.selection_checkbox.setChecked(True)
    assert mock_wells_panel.selection_checkbox.isChecked()


def test_wells_selected_list_can_be_updated(mock_wells_panel):
    assert mock_wells_panel.wells_selection.text() == ""

    mock_wells_panel.wells_selection.setText("1,2,3")
    assert mock_wells_panel.wells_selection.text() == "1,2,3"


def test_get_list_of_selected_wells(mock_wells_panel):
    mock_wells_panel.wells_selection.setText("1,20,54")

    wells_list = mock_wells_panel.get_selected_wells_list()

    assert wells_list == [1, 20, 54]
