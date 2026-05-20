from collections import deque

from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot

from i19serial_ui.parameters.queue import QueueElement

QUEUE_WINDOW_SIZE = (1000, 400)


class CollectionQueueUI(QtWidgets.QWidget):
    """A new window to handle/view to the queue."""

    current_visit = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.resize(*QUEUE_WINDOW_SIZE)
        self.setWindowTitle("Collection Queue")
        self.collection_queue: deque[QueueElement] = deque()
        self._setup_layout()

    def _visit_layout(self):
        vlayout = QtWidgets.QHBoxLayout()
        vlayout.setSpacing(2)
        vlayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl = QtWidgets.QLabel("Current visit:")
        self.visit_txt = QtWidgets.QLabel("")
        vlayout.addWidget(lbl)
        vlayout.addWidget(self.visit_txt)
        return vlayout

    def _setup_layout(self):
        main_layout = QtWidgets.QVBoxLayout()
        visit_layout = self._visit_layout()
        main_layout.addLayout(visit_layout)
        self.setLayout(main_layout)

    @pyqtSlot(str)
    def on_visit_update(self, new_visit: str):
        self.visit_txt.setText(new_visit)

    def update_queue_table(self):
        pass

    def clear_queue_table(self):
        pass
