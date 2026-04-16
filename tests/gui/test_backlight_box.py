from unittest.mock import patch

import pytest

from i19serial_ui.gui.serial_gui_eh2 import SerialGuiEH2


@pytest.fixture
def mock_eh2_gui(qtbot):
    with patch("i19serial_ui.gui.serial_gui_eh2.SerialBlueapiClient"):
        test_gui = SerialGuiEH2()
        qtbot.addWidget(test_gui)
        return test_gui


@pytest.mark.parametrize(
    "plan,mock_params,buttoncalled",
    [
        ("move_backlight_out", {}, "out_button"),
        ("move_backlight_in_via_ui", {}, "in_button"),
        ("move_backlight_in_via_ui_quick", {}, "in_quick_button"),
    ],
)
def test_top_buttons(mock_eh2_gui, plan, mock_params, buttoncalled):
    button = getattr(mock_eh2_gui.backlight, buttoncalled)
    button.click()
    mock_eh2_gui.client.run_plan.assert_called_once_with(plan, mock_params)
