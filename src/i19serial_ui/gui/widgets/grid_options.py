from collections.abc import Callable

from PyQt6 import QtCore, QtGui, QtWidgets

from i19serial_ui.log import LOGGER
from i19serial_ui.parameters.grid import GridType

DEFAULT_GRID = [20, 20]


class GridOptions(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self.current_grid = GridType.POLYMER
        self.grid_size = DEFAULT_GRID
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
        layout.addLayout(
            self._create_text_box_layout(
                self.grid_x, "Grid size X", self._update_grid_x
            )
        )
        layout.addLayout(
            self._create_text_box_layout(
                self.grid_z, "Grid size Z", self._update_grid_z
            )
        )
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
        func: Callable,
        default_value: int = DEFAULT_GRID[0],
    ):
        text_layout = QtWidgets.QVBoxLayout()
        txt_label = QtWidgets.QLabel(label)
        int_validator = QtGui.QIntValidator(0, 100)
        text_box.setValidator(int_validator)
        text_box.setText(str(default_value))
        text_box.setFixedWidth(100)
        text_box.textEdited.connect(func)
        text_layout.addWidget(txt_label)
        text_layout.addWidget(text_box)
        return text_layout

    def _update_grid(self):
        self.current_grid = GridType(self.grid_box.currentText())
        self.logger.info(f"Grid selected: {self.current_grid.value}")

    def _update_grid_x(self):
        # self.grid_x.setText(new_value)
        self.grid_size[0] = int(self.grid_x.text())
        self.logger.warning(f"New grid x value: {self.grid_size}")

    def _update_grid_z(self, new_value):
        self.grid_z.setText(new_value)
        self.logger.warning(f"New grid z value: {self.grid_z.text()}")

    def get_grid_size(self) -> tuple[int, int]:
        _x = int(self.grid_x.text())
        _z = int(self.grid_z.text())
        return (_x, _z)
