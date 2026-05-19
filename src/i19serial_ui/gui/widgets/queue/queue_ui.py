from collections import deque

from PyQt6 import QtWidgets

from i19serial_ui.parameters.queue import QueueElement

QUEUE_WINDOW_SIZE = (1000, 400)
DELETE_BUTTON_STYLE = "QPushButton {color: red; font-weight: bold}"


class CollectionQueueUI(QtWidgets.QWidget):
    def __init__(self, visit: str = ""):
        super().__init__()
        self.resize(*QUEUE_WINDOW_SIZE)
        self.setWindowTitle("Collection Queue")
        self.current_visit = visit
        self.collection_queue: deque[QueueElement] = deque()
        self._setup_layout()

    def _visit_layout(self):
        vlayout = QtWidgets.QHBoxLayout()
        lbl = QtWidgets.QLabel("Current visit:")
        txt = QtWidgets.QLabel(self.current_visit)
        # txt = QtWidgets.QLineEdit()
        # txt.setText(self.current_visit)
        # txt.setReadOnly(True)
        vlayout.addWidget(lbl)
        vlayout.addWidget(txt)
        return vlayout

    def _setup_layout(self):
        main_layout = QtWidgets.QVBoxLayout()
        visit_layout = self._visit_layout()
        main_layout.addLayout(visit_layout)
        self.setLayout(main_layout)
