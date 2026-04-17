from unittest.mock import patch

import pytest

from i19serial_ui.gui.widgets import BacklightBox


@pytest.fixture
def mock_backlight_panel(qtbot):
    with patch("i19serial_ui.gui.serial_gui_eh2.SerialBlueapiClient") as c:
        test_panel = BacklightBox(c)
        qtbot.addWidget(test_panel)
        return test_panel


def test_has_backlight_panel_layout(mock_backlight_panel):
    assert mock_backlight_panel.backlight_layout is not None


def test_backlight_buttons_appear(mock_backlight_panel):
    assert mock_backlight_panel.in_button is not None
    assert mock_backlight_panel.out_button is not None
    assert mock_backlight_panel.in_quick_button is not None
