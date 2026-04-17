from collections.abc import Callable

from PyQt6 import QtCore, QtGui, QtWidgets

from i19serial_ui.blueapi_tools.blueapi_client import SerialBlueapiClient
from i19serial_ui.log import (
    LOGGER,
)
from i19serial_ui.parameters.general_utils import BacklightOption


class BacklightBox(QtWidgets.QWidget):
    def __init__(
        self,
        blueapi_client: SerialBlueapiClient,
        parent: QtWidgets.QWidget | None = None,
    ):
        super().__init__(parent)
        self.logger = LOGGER
        self._create_backlight_buttons()
        self.client = blueapi_client
        self.backlight_layout = self.create_backlight_layout()

    def _create_button(
        self,
        name: str,
        func: Callable,
    ) -> QtWidgets.QPushButton:
        button = QtWidgets.QPushButton(name)
        button.clicked.connect(func)
        return button

    def _create_backlight_buttons(self):
        self.in_button = self._create_button("IN", self.on_click_move_backlight_in)
        self.in_quick_button = self._create_button(
            "QUICK", self.on_click_move_backlight_in_quick
        )
        self.out_button = self._create_button("OUT", self.on_click_move_backlight_out)

    def on_click_move_backlight_out(self):
        LOGGER.info("Moving backlight out")
        self.client.run_plan("move_backlight_out", {})

    def on_click_move_backlight_in(self):
        params = {"option": BacklightOption.SLOW}
        LOGGER.info("Moving backlight in")
        self.client.run_plan("move_backlight_in_via_ui", params)

    def on_click_move_backlight_in_quick(self):
        params = {"option": BacklightOption.QUICK}
        LOGGER.info("Moving backlight in quickly")
        self.client.run_plan("move_backlight_in_via_ui", params)

    def create_backlight_layout(self):
        centre_layout = QtWidgets.QVBoxLayout()
        lgt_label = QtWidgets.QLabel("Backlight:")
        lgt_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        lgt_label.setFont(QtGui.QFont("Arial", 10))
        centre_layout.addWidget(lgt_label)
        centre_layout_bottom = QtWidgets.QVBoxLayout()
        centre_layout_bottom.addWidget(self.in_button)
        centre_layout_bottom.addWidget(self.in_quick_button)
        centre_layout_bottom.addWidget(self.out_button)
        self.in_button.setFixedWidth(75)
        self.in_button.setFixedHeight(15)
        self.in_quick_button.setFixedWidth(75)
        self.in_quick_button.setFixedHeight(15)
        self.out_button.setFixedWidth(75)
        self.out_button.setFixedHeight(15)
        centre_layout.addLayout(centre_layout_bottom)
        centre_layout.setContentsMargins(12, 0, 12, 0)
        centre_layout.addStretch()
        return centre_layout
