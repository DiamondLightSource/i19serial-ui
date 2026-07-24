from unittest.mock import patch

import pytest
from PyQt6 import QtWidgets

from i19serial_ui.gui.widgets.login_dialog import LoginDialog


@pytest.fixture
def mock_login_dialog(qtbot):
    with patch(
        "i19serial_ui.gui.widgets.login_dialog.SerialBlueapiClient"
    ) as mock_client:
        test_dialog = LoginDialog(mock_client)
        qtbot.addWidget(test_dialog)
        return test_dialog


def test_login_dialog(mock_login_dialog):
    assert mock_login_dialog.layout()
    assert isinstance(mock_login_dialog.layout(), QtWidgets.QVBoxLayout)
    assert mock_login_dialog.layout().count() == 2


def test_button_click_calls_blueapi_login(mock_login_dialog):
    mock_login_dialog.btn.click()

    mock_login_dialog.client.client.login.assert_called_once()
