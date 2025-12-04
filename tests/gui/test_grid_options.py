import pytest
from PyQt6 import QtWidgets

from i19serial_ui.gui.widgets.grid_options import GridOptions
from i19serial_ui.parameters.grid import GridType


@pytest.fixture
def mock_grid_panel(qtbot):
    test_panel = GridOptions()
    qtbot.addWidget(test_panel)
    return test_panel


def test_grid_options_panel(mock_grid_panel):
    assert mock_grid_panel.grid_layout is not None
    assert isinstance(mock_grid_panel.grid_layout, QtWidgets.QHBoxLayout)


def test_update_grid_size_boxes(mock_grid_panel):
    assert isinstance(mock_grid_panel.grid_layout.children()[0], QtWidgets.QVBoxLayout)

    assert mock_grid_panel.grid_x.text() == "20"
    assert mock_grid_panel.grid_z.text() == "20"

    mock_grid_panel.grid_x.setText("10")
    mock_grid_panel.grid_z.setText("5")

    assert mock_grid_panel.grid_x.text() == "10"
    assert mock_grid_panel.grid_z.text() == "5"


def test_change_selection_in_combo_box_updates_current_grid(mock_grid_panel):
    assert mock_grid_panel.grid_box.currentText() == GridType.POLYMER

    mock_grid_panel.grid_box.setCurrentText(GridType.FILM)

    assert mock_grid_panel.grid_box.currentText() == GridType.FILM
    assert mock_grid_panel.current_grid == GridType.FILM
