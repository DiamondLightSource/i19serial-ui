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
        (
            "rotate_in_phi",
            {"rot_axis_increment": 10},
            "phiadjusterpositive",
        ),
        (
            "rotate_in_phi",
            {"rot_axis_increment": -10},
            "phiadjusternegative",
        ),
    ],
)
def test_top_buttons(mock_eh2_gui, plan, mock_params, buttoncalled):
    button = getattr(mock_eh2_gui.phi_rotator, buttoncalled)
    button.click()
    mock_eh2_gui.client.run_plan.assert_called_once_with(plan, mock_params)
