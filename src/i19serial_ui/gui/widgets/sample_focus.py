from PyQt6 import QtCore, QtGui, QtWidgets

from i19serial_ui.blueapi_tools.blueapi_client import SerialBlueapiClient
from i19serial_ui.log import LOGGER

# Wrapper around bps.mv from dodal.plan_stubs
MOVE_PLAN = "move"


class SampleFocus(QtWidgets.QWidget):
    def __init__(
        self,
        blueapi_client: SerialBlueapiClient,
        parent: QtWidgets.QWidget | None = None,
    ):
        super().__init__(parent)
        self.client = blueapi_client
        self.init_buttons()
        self.focus_layout = self.create_focus_layout()

    def init_buttons(self):
        self.in_small = self._create_button("in", 0.005)
        self.in_large = self._create_button("IN", 0.05)
        self.out_small = self._create_button("out", -0.005)
        self.out_large = self._create_button("OUT", -0.05)

    def create_focus_layout(self):
        layout = QtWidgets.QVBoxLayout()
        lbl = QtWidgets.QLabel("Focus")
        lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        lbl.setFont(QtGui.QFont("Arial", 10))
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addWidget(self.out_large)
        btn_layout.addWidget(self.out_small)
        btn_layout.addWidget(self.in_small)
        btn_layout.addWidget(self.in_large)
        btn_layout.setSpacing(5)
        layout.addWidget(lbl)
        layout.addLayout(btn_layout)
        layout.setSpacing(10)
        layout.addStretch()
        return layout

    def _create_button(
        self, name: str, distance_mm: float, size: tuple[int, int] = (20, 30)
    ):
        btn = QtWidgets.QPushButton(name)
        btn.setMaximumHeight(size[0])
        btn.setMaximumWidth(size[1])
        btn.clicked.connect(lambda: self._on_click_run_move_plan(distance_mm))
        return btn

    def _on_click_run_move_plan(self, distance_mm: float):
        LOGGER.info(f"Move focus (y) by {distance_mm}")
        # WHO KNOWS
        self.client.run_plan(MOVE_PLAN, {"moves": {"serial_stages.y": distance_mm}})
