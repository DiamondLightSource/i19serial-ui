from collections import deque
from typing import Any, Literal

from pydantic.dataclasses import dataclass
from PyQt6 import QtWidgets

QUEUE_WINDOW_SIZE = (1000, 400)
DELETE_BUTTON_STYLE = "QPushButton {color: red; font-weight: bold}"

LABELS = [
    "visit",
    "dataset",
    "prefix",
    "num images",
    "exposure time (s)",
    "image width",
    "detector distance (mm)",
    "two theta (deg)",
    "transmission (%)",
    "well start",
    "well end",
    "well selection",
    "series length",
    "oscillation",
    "oscillation time (s)",
]


@dataclass
class QueueElement:
    plan_name: str
    plan_params: dict[str, Any]


class CollectionTable(QtWidgets.QTableWidget):
    """A table widget to display the queued collections."""

    def __init__(self, rows, columns, parent):
        super().__init__(rows, columns, parent)


class QueueTable(QtWidgets.QTableWidget):
    """A table widget to queue up plans."""

    def __init__(self, parent):
        super().__init__(parent)
        self._setup_table()

    def _setup_table(self):
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(["Queued items", "Remove from queue"])

    def _create_delete_button(self, collection_to_delete):
        btn = QtWidgets.QPushButton("X")
        btn.setStyleSheet(DELETE_BUTTON_STYLE)
        btn.clicked.connect(
            lambda: self.update_table(collection_to_delete, action="remove")
        )
        return btn

    def update_table(self, collection, action: Literal["add", "remove"]):
        pass


class CollectionQueueUI(QtWidgets.QWidget):
    def __init__(self, visit: str):
        super().__init__()
        self.resize(*QUEUE_WINDOW_SIZE)
        self.setWindowTitle("Collection Queue")
        self.current_visit = visit
        self.collection_queue: deque[QueueElement] = deque()
        self._setup_layout()

    def _setup_layout(self):
        pass
