from collections.abc import Callable

from PyQt6 import QtWidgets


class CoordinateSystemPanel(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)

    def create_layout(self):
        pass

    def _setup_positions_layout(self):
        pass

    def _setup_main_buttons_layout(self):
        pass

    def _setup_side_buttons_layout(self):
        pass

    def _create_button(
        self,
        name: str,
        func: Callable,
    ) -> QtWidgets.QPushButton:
        button = QtWidgets.QPushButton(name)
        button.clicked.connect(func)
        return button
