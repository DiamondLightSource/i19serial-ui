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


def test_refresh_login_state_to_login(mock_login_dialog, qtbot):
    mock_login_dialog._update_user_fedid = MagicMock(return_value=None)
    mock_login_dialog._on_click_trigger_login = MagicMock()

    mock_login_dialog.show()

    assert mock_login_dialog.auth_btn.text() == "LOGIN"
    assert mock_login_dialog.lbl.text() == "Please log in to run"

    mock_login_dialog.auth_btn.click()
    mock_login_dialog._on_click_trigger_login.assert_called_once()


def test_refresh_login_state_to_logout(mock_login_dialog, qtbot):
    mock_login_dialog._update_user_fedid = MagicMock(return_value="abc12345")
    mock_login_dialog._on_click_trigger_logout = MagicMock()

    mock_login_dialog.show()

    assert mock_login_dialog.auth_btn.text() == "LOGOUT"
    assert mock_login_dialog.lbl.text() == "Logged in as abc12345"

    mock_login_dialog.auth_btn.click()
    mock_login_dialog._on_click_trigger_logout.assert_called_once()


def test_on_click_trigger_login(mock_login_dialog, qtbot):
    mock_login_dialog._update_user_fedid = MagicMock(return_value="abc1234")
    mock_login_dialog.close = MagicMock()

    with qtbot.waitSignal(mock_login_dialog.user_fedid) as sig:
        mock_login_dialog._on_click_trigger_login()

        mock_login_dialog.client.client.login.assert_called_once()
        assert sig.args[0] == "abc1234"
        mock_login_dialog.close.assert_called_once()
        assert mock_login_dialog.user_logged_in


def test_on_click_trigger_logout(mock_login_dialog, qtbot):
    mock_login_dialog.close = MagicMock()

    with qtbot.waitSignal(mock_login_dialog.user_fedid) as sig:
        mock_login_dialog._on_click_trigger_logout()

        mock_login_dialog.client.client.logout.assert_called_once()
        assert sig.args[0] == ""
        mock_login_dialog.close.assert_called_once()
        assert not mock_login_dialog.user_logged_in


def test_get_session_manager_returns_none_if_never_been_logged_in(
    mock_login_dialog, qtbot
):
    mock_login_dialog.client.get_blueapi_auth_token_path = MagicMock(return_value=None)

    res = mock_login_dialog._get_session_manager()

    assert not res
