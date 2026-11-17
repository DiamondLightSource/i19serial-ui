from unittest.mock import patch

import pytest
from PyQt6 import QtWidgets

from i19serial_ui.gui.widgets.phi_rotator import PhiAdjust


@pytest.fixture
def mock_phi_panel(qtbot):
    with patch("i19serial_ui.gui.serial_gui_eh2.SerialBlueapiClient") as mock_client:
        test_panel = PhiAdjust(mock_client)
        qtbot.addWidget(test_panel)
        return test_panel


def test_has_phi_panel_layout(mock_phi_panel):
    assert mock_phi_panel.phirotator_layout is not None


def test_default_present_and_buttons(mock_phi_panel):
    assert mock_phi_panel.phianglebox.text() == "10"
    btn_pos = mock_phi_panel.phiadjusterpositive
    assert btn_pos and isinstance(btn_pos, QtWidgets.QPushButton)
    btn_neg = mock_phi_panel.phiadjusternegative
    assert btn_neg and isinstance(btn_neg, QtWidgets.QPushButton)


def test_click_negative_rotation(mock_phi_panel):
    mock_phi_panel.phianglebox.setText("2")
    expected_motor = "serial_stages.phi"
    expected_rotation = -2

    mock_phi_panel.phiadjusternegative.click()

    mock_phi_panel.client.run_plan.assert_called_once_with(
        "move_relative", {"moves": {expected_motor: expected_rotation}}
    )


def test_click_positive_rotation(mock_phi_panel):
    mock_phi_panel.phianglebox.setText("5")
    expected_motor = "serial_stages.phi"
    expected_rotation = 5

    mock_phi_panel.phiadjusterpositive.click()

    mock_phi_panel.client.run_plan.assert_called_once_with(
        "move_relative", {"moves": {expected_motor: expected_rotation}}
    )
