from PyQt6 import QtCore, QtWidgets

from i19serial_ui.log import LOGGER
from i19serial_ui.parameters.grid import GridType


class GridOptions(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.current_grid = GridType.POLYMER
        self.logger = LOGGER
        self.init_options()
        self.grid_layout = self.create_layout()

    def init_options(self):
        self.grid_box = QtWidgets.QComboBox()
        self.grid_box.addItems(list(GridType))
        self.grid_box.setCurrentText(self.current_grid)
        self.grid_box.currentIndexChanged.connect(self._update_grid)
        self.grid_x = QtWidgets.QLineEdit()
        self.grid_z = QtWidgets.QLineEdit()

    def create_layout(self):
        layout = QtWidgets.QHBoxLayout()
        layout.addLayout(self._create_dropdown_layout())
        layout.addLayout(self._create_text_box_layout(self.grid_x, "Grid size X"))
        layout.addLayout(self._create_text_box_layout(self.grid_z, "Grid size Z"))
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        return layout

    def _create_dropdown_layout(self):
        drop_layout = QtWidgets.QVBoxLayout()
        self.grid_box.setFixedWidth(100)
        drop_label = QtWidgets.QLabel("Grid options")
        drop_layout.addWidget(drop_label)
        drop_layout.addWidget(self.grid_box)
        return drop_layout

    def _create_text_box_layout(
        self,
        text_box: QtWidgets.QLineEdit,
        label: str,
        default_value: int = 20,
    ):
        text_layout = QtWidgets.QVBoxLayout()
        txt_label = QtWidgets.QLabel(label)
        text_box.setText(str(default_value))
        text_box.setFixedWidth(100)
        text_layout.addWidget(txt_label)
        text_layout.addWidget(text_box)
        return text_layout

    def _update_grid(self):
        self.current_grid = self.grid_box.currentText()
        self.logger.info(f"Grid selected: {self.current_grid}")
