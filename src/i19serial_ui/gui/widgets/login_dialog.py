import base64
from pathlib import Path

from PyQt6 import QtGui, QtWidgets
from PyQt6.QtCore import Qt, pyqtSignal

from i19serial_ui.blueapi_tools.blueapi_client import SerialBlueapiClient
from i19serial_ui.log import LOGGER, log_to_gui

DIALOG_SIZE = (150, 80)

BLUAPI_CACHE_DIR = Path("~/.cache/blueapi_cache").expanduser()


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

    @property
    def _token_path(self) -> str:
        return BLUAPI_CACHE_DIR.as_posix()

    def create_layout(self):
        layout = QtWidgets.QVBoxLayout()
        lbl = QtWidgets.QLabel("Please log in to run")
        lbl.setFont(QtGui.QFont("Arial", 10))
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.btn = QtWidgets.QPushButton("LOGIN")
        self.btn.setMaximumHeight(20)
        self.btn.setMaximumWidth(50)
        self.btn.clicked.connect(self._on_click_trigger_login)
        layout.addWidget(lbl)
        layout.addWidget(self.btn)
        self.setLayout(layout)

    def load_token(self) -> str:
        with open(self._token_path, "rb") as fh:
            token = base64.b64decode(fh.read()).decode("utf-8")
        return token

    def _update_user_fedid(self) -> str:
        return "boh"

    def _on_click_trigger_login(self):
        try:
            self.client.client.login()
            self.user_fedid.emit(self._update_user_fedid())
        except Exception as e:
            log_to_gui(self.logger, "Login failed", level="ERROR")
            self.logger.error("Login failed")
            self.logger.exception(e)
