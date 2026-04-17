from collections.abc import Callable

from PyQt6 import QtCore, QtGui, QtWidgets

from i19serial_ui.blueapi_tools.blueapi_client import SerialBlueapiClient
from i19serial_ui.log import (
    LOGGER,
)


class PhiAdjust(QtWidgets.QWidget):
    def __init__(
        self,
        blueapi_client: SerialBlueapiClient,
        parent: QtWidgets.QWidget | None = None,
    ):
        super().__init__(parent)
        self.logger = LOGGER
        self._create_adjuster()
        self.client = blueapi_client
        self.phirotator_layout = self.create_phirotator_layout()

    def _create_button(
        self,
        name: str,
        func: Callable,
    ) -> QtWidgets.QPushButton:
        button = QtWidgets.QPushButton(name)
        button.clicked.connect(func)
        return button

    def _create_adjuster(self):
        self.phiadjusterpositive = self._create_button(
            "+", self.on_click_move_phi_deg_pos
        )
        self.phiadjusternegative = self._create_button(
            "-", self.on_click_move_phi_deg_neg
        )
        self.phianglebox = QtWidgets.QLineEdit()
        inputvalidator = QtGui.QRegularExpressionValidator(
            QtCore.QRegularExpression("[0-9][0-9]"), self.phianglebox
        )
        self.phianglebox.setValidator(inputvalidator)

    def create_phirotator_layout(self):
        right_layout = QtWidgets.QVBoxLayout()
        adj_label = QtWidgets.QLabel("Phi Rotation:")
        adj_label.setFont(QtGui.QFont("Arial", 10))
        right_layout_bottom = QtWidgets.QHBoxLayout()
        right_layout.addWidget(adj_label)
        right_layout_bottom.addWidget(self.phiadjusterpositive)
        right_layout_bottom.addWidget(self.phianglebox)
        right_layout_bottom.addWidget(self.phiadjusternegative)
        self.phianglebox.setText("10")
        self.phiadjusternegative.setFixedWidth(25)
        self.phianglebox.setFixedWidth(25)
        self.phiadjusterpositive.setFixedWidth(25)
        right_layout.addLayout(right_layout_bottom)
        right_layout.setContentsMargins(12, 12, 12, 0)
        right_layout.addStretch()
        return right_layout

    def on_click_move_phi_deg_pos(self):
        rotation_increment = float(self.phianglebox.text())
        params = {
            "rot_increment": rotation_increment,
        }
        LOGGER.info(f"Rotating {params['rot_increment']} in phi")
        self.client.run_plan("rotate_in_phi", params)

    def on_click_move_phi_deg_neg(self):
        rotation_increment = -float(self.phianglebox.text())
        params = {
            "rot_increment": rotation_increment,
        }
        LOGGER.info(f"Rotating {params['rot_increment']} in phi")
        self.client.run_plan("rotate_in_phi", params)
