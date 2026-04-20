from unittest.mock import patch

import pytest

from i19serial_ui.gui.widgets.phi_rotator import PhiAdjust


@pytest.fixture
def mock_phi_panel(qtbot):
    with patch("i19serial_ui.gui.serial_gui_eh2.SerialBlueapiClient") as c:
        test_panel = PhiAdjust(c)
        qtbot.addWidget(test_panel)
        return test_panel


def test_has_phi_panel_layout(mock_phi_panel):
    assert mock_phi_panel.phirotator_layout is not None


def test_default_present_and_buttons(mock_phi_panel):
    assert mock_phi_panel.phianglebox.text() == "10"
    assert mock_phi_panel.phiadjusterpositive is not None
    assert mock_phi_panel.phiadjusternegative is not None
