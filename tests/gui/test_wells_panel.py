import pytest

from i19serial_ui.gui.wells_selection import WellsSelectionPanel


@pytest.fixture
def mock_wells_panel(qtbot):
    test_panel = WellsSelectionPanel()
    qtbot.addWidget(test_panel)
    return test_panel


def test_wells_selection_panel(mock_wells_selection):
    pass


def test_selection_checkbox():
    pass
