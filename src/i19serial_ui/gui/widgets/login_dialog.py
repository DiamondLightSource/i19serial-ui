from pathlib import Path

from blueapi.service import SessionManager
from PyQt6 import QtGui, QtWidgets
from PyQt6.QtCore import Qt, pyqtSignal

from i19serial_ui.blueapi_tools.blueapi_client import SerialBlueapiClient
from i19serial_ui.log import LOGGER, log_to_gui

DIALOG_SIZE = (150, 80)

BLUAPI_CACHE_DIR = Path("~/.cache/blueapi_cache").expanduser()

USER_ID_CLAIM = "fedid"
# NOTE User will be automatically logged out after ~5 days
# So they'll need to log back in if beamtime is longer than that


class LoginDialog(QtWidgets.QWidget):
    user_fedid = pyqtSignal(str)

    def __init__(self, client: SerialBlueapiClient):
        super().__init__()
        self.resize(*DIALOG_SIZE)
        self.setWindowTitle("Blueapi login")
        self.logger = LOGGER
        self.client = client
        self.create_layout()

    # @property
    # def _token_path(self) -> str:
    #     return BLUAPI_CACHE_DIR.as_posix()

    # def create_layout(self):
    #     layout = QtWidgets.QGridLayout()  # .QVBoxLayout()
    #     lbl = QtWidgets.QLabel("Please log in to run")
    #     lbl.setFont(QtGui.QFont("Arial", 10))
    #     lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
    #     self.login_btn = QtWidgets.QPushButton("LOGIN")
    #     self.login_btn.setMaximumHeight(20)
    #     self.login_btn.setMaximumWidth(60)
    #     self.login_btn.clicked.connect(self._on_click_trigger_login)
    #     self.logout_btn = QtWidgets.QPushButton("LOGOUT")
    #     self.logout_btn.setMaximumHeight(20)
    #     self.logout_btn.setMaximumWidth(60)
    #     self.logout_btn.clicked.connect(self._on_click_trigger_logout)
    #     layout.addWidget(lbl, 0, 0, 1, 2)
    #     layout.addWidget(self.login_btn, 1, 0)
    #     layout.addWidget(self.logout_btn, 1, 1)
    #     self.setLayout(layout)

    # def _load_access_token(self) -> str:
    #     with open(self._token_path, "rb") as fh:
    #         token = base64.b64decode(fh.read()).decode("utf-8")
    #     return token

    # def _decode_access_token(self) -> dict[str, Any]:
    #     # NOTE Proper way would be to get the jwt_uri from keycloak
    #     # But since blueapi will do the verification and we just need to read the fedid
    #     # this may just be enoug
    #     token = self._load_access_token()
    #     payload = jwt.decode(token, options={"verify_signature": False})
    #     return payload

    # def _update_user_fedid(self) -> str:
    #     access_token = self._decode_access_token()
    #     if not access_token:
    #         raise ValueError("Could not get access token")
    #     return access_token.get("fedid")  # type: ignore
    def _get_session_manager(self) -> SessionManager | None:
        try:
            return SessionManager.from_cache(
                auth_token_path=self.client._blueapi_config.auth_token_path  # noqa: SLF001
            )
        except Exception:
            # No cached session yet, i.e. user has never logged in
            # print(auth)
            print(self.client._blueapi_config.auth_token_path)
            return None

    def _update_user_fedid(self) -> str | None:
        sm = self._get_session_manager()
        if sm is not None and (access_token := sm.get_valid_access_token()) != "":
            # Logged In
            # Get fedid
            print(access_token)
            return sm.decode_jwt(access_token).get(USER_ID_CLAIM)

    def create_layout(self):
        layout = QtWidgets.QVBoxLayout()
        self.lbl = QtWidgets.QLabel()
        self.lbl.setFont(QtGui.QFont("Arial", 10))
        self.lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.auth_btn = QtWidgets.QPushButton()
        self.auth_btn.setMaximumHeight(20)
        layout.addWidget(self.lbl)
        layout.addWidget(self.auth_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)
        self._refresh_login_state()

    def _refresh_login_state(self):
        if (fedid := self._update_user_fedid()) is None:
            # Not logged in
            self.lbl.setText("Please log in to run")
            self.auth_btn.setText("LOGIN")
            trigger = self._on_click_trigger_login
        else:
            self.lbl.setText(f"Logged in as {fedid}")
            self.auth_btn.setText("LOGOUT")
            trigger = self._on_click_trigger_logout

        try:
            self.auth_btn.clicked.disconnect()
        except TypeError:
            # Not connected to anything yet
            pass
        self.auth_btn.clicked.connect(trigger)

    def showEvent(self, a0: QtGui.QShowEvent | None):  # noqa: N802
        self._refresh_login_state()
        super().showEvent(a0)

    def _on_click_trigger_login(self):
        try:
            self.client.client.login()
            self.user_fedid.emit(self._update_user_fedid())
            self.close()
        except Exception as e:
            log_to_gui(self.logger, "Login failed", level="ERROR")
            self.logger.exception(e)

    def _on_click_trigger_logout(self):
        try:
            self.client.client.logout()
            self.user_fedid.emit("")
            self.close()
        except Exception as e:
            log_to_gui(self.logger, "Logout failed", level="ERROR")
            self.logger.exception(e)
