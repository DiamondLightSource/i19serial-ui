from collections import deque

from PyQt6 import QtWidgets

from i19serial_ui.parameters.queue import QueueElement


class QueueTable(QtWidgets.QTableWidget):
    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self.queue: deque[QueueElement] = deque()  # easier with a signal tbh
