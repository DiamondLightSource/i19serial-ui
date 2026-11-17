from collections.abc import Callable
from enum import IntEnum

from PyQt6 import QtCore, QtGui, QtWidgets

from i19serial_ui.blueapi_tools.blueapi_client import SerialBlueapiClient
from i19serial_ui.log import (
    LOGGER,
)

# Wrapper around bps.mv from dodal.plan_stubs
MOVE_PLAN = "move_relative"


class RotationDirection(IntEnum):
    POSITIVE = 1
    NEGATIVE = -1


class PhiAdjust(QtWidgets.QWidget):
    def __init__(
        self,
        blueapi_client: SerialBlueapiClient,
        parent: QtWidgets.QWidget | None = None,
    ):
        super().__init__(parent)
        self.logger = LOGGER
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
            "+", lambda: self._on_click_run_plan_to_rotate(RotationDirection.POSITIVE)
        )
        self.phiadjusternegative = self._create_button(
            "-", lambda: self._on_click_run_plan_to_rotate(RotationDirection.NEGATIVE)
        )
        self.phianglebox = QtWidgets.QLineEdit()
        self.phianglebox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        inputvalidator = QtGui.QRegularExpressionValidator(
            QtCore.QRegularExpression(r"[1-3]?[\d]?[\d](\.\d\d|\.\d|)"),
            self.phianglebox,
        )
        self.phianglebox.setValidator(inputvalidator)

    def create_phirotator_layout(self):
        self._create_adjuster()
        right_layout = QtWidgets.QVBoxLayout()
        adj_label = QtWidgets.QLabel("Phi Rotation:")
        adj_label.setFont(QtGui.QFont("Arial", 10))
        adj_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        right_layout_bottom = QtWidgets.QHBoxLayout()
        right_layout.addWidget(adj_label)
        right_layout_bottom.addWidget(self.phiadjusterpositive)
        right_layout_bottom.addWidget(self.phianglebox)
        right_layout_bottom.addWidget(self.phiadjusternegative)
        self.phianglebox.setText("10")
        self.phiadjusternegative.setFixedWidth(25)
        self.phianglebox.setFixedWidth(50)  # Should be larger
        self.phiadjusterpositive.setFixedWidth(25)
        right_layout.addLayout(right_layout_bottom)
        right_layout.setSpacing(10)
        right_layout.addStretch()
        return right_layout

    def _on_click_run_plan_to_rotate(self, direction: RotationDirection):
        rotation_deg = float(self.phianglebox.text()) * direction.value
        LOGGER.info(f"Rotating phi axis by {rotation_deg} deg.")
        self.client.run_plan(MOVE_PLAN, {"moves": {"serial_stages.phi": rotation_deg}})
