from unittest.mock import MagicMock, patch

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


def test_button_click_calls_blueapi_login(mock_login_dialog, qtbot):
    mock_login_dialog._update_user_fedid = MagicMock(return_value="abc1234")
    with qtbot.waitSignal(mock_login_dialog.user_fedid) as sig:
        mock_login_dialog.btn.click()

        mock_login_dialog.client.client.login.assert_called_once()
        assert sig.args[0] == "abc1234"


def test_update_fedid_raises_error_if_access_token_not_found(mock_login_dialog):
    mock_login_dialog._decode_access_token = MagicMock(return_value=None)
    with pytest.raises(ValueError):
        mock_login_dialog._update_user_fedid()
