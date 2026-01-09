from collections.abc import Callable

from PyQt6 import QtGui, QtWidgets

from i19serial_ui.blueapi_tools.blueapi_client import SerialBlueapiClient
from i19serial_ui.gui.ui_utils import image_file_path
from i19serial_ui.log import LOGGER


def placeholder_run_btn(s: str):
    LOGGER.info(s)


class CoordinateSystemPanel(QtWidgets.QWidget):
    def __init__(
        self,
        blueapi_client: SerialBlueapiClient,
        parent: QtWidgets.QWidget | None = None,
    ):
        super().__init__(parent)
        self.client = blueapi_client
        self.init_buttons()
        self.init_text_boxes()
        self.cs_layout = self.create_layout()

    def create_layout(self):
        main_layout = QtWidgets.QVBoxLayout()
        positions_layout = self._setup_positions_layout()
        buttons_layout = self._setup_main_buttons_layout()
        main_layout.addLayout(positions_layout)
        main_layout.addLayout(buttons_layout)
        return main_layout

    def init_buttons(self):
        self.make_btn = self._create_button(
            "Macke coordinate system", lambda: placeholder_run_btn("CS MAKER")
        )
        self.test_btn = self._create_button(
            "Test", lambda: placeholder_run_btn("CS TEST")
        )
        self.clear_btn = self._create_button(
            "Clear", lambda: placeholder_run_btn("CLEAR")
        )
        self.save_btn = self._create_button("Save", lambda: placeholder_run_btn("SAVE"))
        self.upload_btn = self._create_button(
            "Upload", lambda: placeholder_run_btn("UPLOAD")
        )

    def init_text_boxes(self):
        self.top_left_x = QtWidgets.QLineEdit()
        self.top_left_y = QtWidgets.QLineEdit()
        self.top_left_z = QtWidgets.QLineEdit()
        self.top_right_x = QtWidgets.QLineEdit()
        self.top_right_y = QtWidgets.QLineEdit()
        self.top_right_z = QtWidgets.QLineEdit()
        self.bottom_left_x = QtWidgets.QLineEdit()
        self.bottom_left_y = QtWidgets.QLineEdit()
        self.bottom_left_z = QtWidgets.QLineEdit()

    def _fiducial_layout(
        self, position: str, icon_path: str, text_boxes: list[QtWidgets.QLineEdit]
    ):
        pos_layout = QtWidgets.QHBoxLayout()
        pixmap = QtGui.QPixmap(icon_path)
        pixmap.scaledToWidth(30)
        pixmap.scaledToHeight(30)
        icon = QtWidgets.QLabel()
        icon.setFixedSize(30, 30)
        icon.setPixmap(pixmap)
        icon.setScaledContents(True)
        btn = self._create_button(
            f"Set {position}", lambda: placeholder_run_btn(f"SET {position.upper()}")
        )
        btn.setFixedWidth(120)
        pos_layout.addWidget(icon)
        pos_layout.addWidget(btn)
        pos_layout.addWidget(text_boxes[0])
        pos_layout.addWidget(text_boxes[1])
        pos_layout.addWidget(text_boxes[2])
        return pos_layout

    def _setup_positions_layout(self):
        layout = QtWidgets.QGridLayout()
        layout.addLayout(
            self._fiducial_layout(
                "top left",
                image_file_path("TL.png"),
                [self.top_left_x, self.top_left_y, self.top_left_z],
            ),
            0,
            0,
        )
        layout.addLayout(
            self._fiducial_layout(
                "top right",
                image_file_path("TR.png"),
                [self.top_right_x, self.top_right_y, self.top_right_z],
            ),
            1,
            0,
        )
        layout.addLayout(
            self._fiducial_layout(
                "bottom left",
                image_file_path("BL.png"),
                [self.bottom_left_x, self.bottom_left_y, self.bottom_left_z],
            ),
            2,
            0,
        )
        return layout

    def _setup_main_buttons_layout(self):
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.make_btn)
        layout.addWidget(self.test_btn)
        layout.addWidget(self.clear_btn)
        layout.addWidget(self.save_btn)
        layout.addWidget(self.upload_btn)
        return layout

    def _create_button(
        self,
        name: str,
        func: Callable,
    ) -> QtWidgets.QPushButton:
        button = QtWidgets.QPushButton(name)
        button.clicked.connect(func)
        return button

    def _update_xyz(self):
        pass
