from enum import StrEnum

from PyQt6 import QtCore, QtGui, QtWidgets

from i19serial_ui.blueapi_tools.blueapi_client import SerialBlueapiClient
from i19serial_ui.gui.ui_utils import create_image_icon, image_file_path
from i19serial_ui.log import LOGGER

# Wrapper around bps.mv from dodal.plan_stubs
MOVE_PLAN = "move"


class NudgeDirection(StrEnum):
    X = "x"
    Z = "z"


class SampleAlignment(QtWidgets.QWidget):
    def __init__(
        self,
        blueapi_client: SerialBlueapiClient,
        parent: QtWidgets.QWidget | None = None,
    ):
        super().__init__(parent)
        self.client = blueapi_client
        self.init_arrow_buttons()
        self.arrow_layout = self.create_layout()

    def init_arrow_buttons(self):
        # Z direction
        self.up_large = self._create_icon_button(
            self._get_btn_icon("arrow_up_large.png"), 0.01, NudgeDirection.Z
        )
        self.up_small = self._create_icon_button(
            self._get_btn_icon("arrow_up.png"), 0.002, NudgeDirection.Z
        )
        self.down_large = self._create_icon_button(
            self._get_btn_icon("arrow_down_large.png"), -0.01, NudgeDirection.Z
        )
        self.down_small = self._create_icon_button(
            self._get_btn_icon("arrow_down.png"), -0.002, NudgeDirection.Z
        )
        # X firection
        self.right_large = self._create_icon_button(
            self._get_btn_icon("arrow_right_large.png"), 0.01, NudgeDirection.X
        )
        self.right_small = self._create_icon_button(
            self._get_btn_icon("arrow_right.png"), 0.002, NudgeDirection.X
        )
        self.left_large = self._create_icon_button(
            self._get_btn_icon("arrow_left_large.png"), -0.01, NudgeDirection.X
        )
        self.left_small = self._create_icon_button(
            self._get_btn_icon("arrow_left.png"), -0.002, NudgeDirection.X
        )

    def create_layout(self):
        stage_lbl = QtWidgets.QLabel()
        stage_lbl.setPixmap(QtGui.QPixmap(image_file_path("stages.png")))
        stage_lbl.setMaximumSize(25, 25)
        stage_lbl.setScaledContents(True)
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.up_large, 0, 2)
        layout.addWidget(self.up_small, 1, 2)
        layout.addWidget(self.left_large, 2, 0)
        layout.addWidget(self.left_small, 2, 1)
        layout.addWidget(stage_lbl, 2, 2)
        layout.addWidget(self.right_large, 2, 4)
        layout.addWidget(self.right_small, 2, 3)
        layout.addWidget(self.down_large, 4, 2)
        layout.addWidget(self.down_small, 3, 2)
        layout.setHorizontalSpacing(1)
        layout.setContentsMargins(10, 10, 10, 10)
        return layout

    def _get_btn_icon(self, icon_name: str) -> QtGui.QIcon:
        icon_path = image_file_path(icon_name)
        icon = create_image_icon(icon_path)
        return icon

    def _create_icon_button(
        self, icon: QtGui.QIcon, distance_mm: float, direction: NudgeDirection
    ) -> QtWidgets.QPushButton:
        icon_button = QtWidgets.QPushButton("")
        icon_button.setIcon(icon)
        icon_button.setIconSize(QtCore.QSize(25, 25))
        icon_button.setMaximumWidth(25)
        icon_button.setMaximumHeight(25)
        icon_button.setFlat(True)
        icon_button.clicked.connect(
            lambda: self._on_click_run_move_plan(distance_mm, direction)
        )
        return icon_button

    def _on_click_run_move_plan(self, distance_mm: float, direction: NudgeDirection):
        LOGGER.info(f"Nudge {direction.value} sample by {distance_mm}")
        match direction:
            case NudgeDirection.X:
                self.client.run_plan(
                    MOVE_PLAN, {"moves": {"serial_stages.x": distance_mm}}
                )
            case NudgeDirection.Z:
                self.client.run_plan(
                    MOVE_PLAN, {"moves": {"serial_stages.z": distance_mm}}
                )
