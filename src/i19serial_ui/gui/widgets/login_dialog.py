from PyQt6 import QtGui, QtWidgets
from PyQt6.QtCore import Qt

from i19serial_ui.blueapi_tools.blueapi_client import SerialBlueapiClient
from i19serial_ui.log import LOGGER

DIALOG_SIZE = (150, 80)


# NOTE There is no logout on the UI, will need to remember to do that manually


class LoginDialog(QtWidgets.QWidget):
    def __init__(self, client: SerialBlueapiClient):
        super().__init__()
        self.resize(*DIALOG_SIZE)
        self.setWindowTitle("Blueapi login")
        self.logger = LOGGER
        self.client = client
        self.create_layout()

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

    def _on_click_trigger_login(self):
        try:
            self.client.client.login()
        except Exception as e:
            self.logger.error("Login failed")
            self.logger.exception(e)
