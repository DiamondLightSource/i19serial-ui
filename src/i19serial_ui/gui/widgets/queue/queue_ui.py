from collections import deque
from typing import Literal

from PyQt6 import QtGui, QtWidgets
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot

from i19serial_ui.gui.widgets.queue.queue_table import QueueTable
from i19serial_ui.log import LOGGER
from i19serial_ui.parameters.queue import QueueElement

QUEUE_WINDOW_SIZE = (800, 300)


class CollectionQueueUI(QtWidgets.QWidget):
    """A new window to handle/view to the queue."""

    current_visit = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.resize(*QUEUE_WINDOW_SIZE)
        self.setWindowTitle("Collection Queue")
        self.logger = LOGGER
        self.run_queue: deque[QueueElement] = deque()
        self.table = QueueTable(self)
        self._setup_layout()

    def _visit_layout(self):
        vlayout = QtWidgets.QHBoxLayout()
        vlayout.setSpacing(2)
        vlayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl = QtWidgets.QLabel("Current visit:")
        lbl.setFont(QtGui.QFont("Arial", 10))
        self.visit_txt = QtWidgets.QLabel("")
        self.visit_txt.setFont(QtGui.QFont("Arial", 10))
        vlayout.addWidget(lbl)
        vlayout.addWidget(self.visit_txt)
        return vlayout

    def _setup_layout(self):
        main_layout = QtWidgets.QVBoxLayout()
        visit_layout = self._visit_layout()
        main_layout.addLayout(visit_layout)
        main_layout.addWidget(self.table)
        self.setLayout(main_layout)

    @pyqtSlot(str)
    def on_visit_update(self, new_visit: str):
        self.visit_txt.setText(new_visit)

    def update_queue_table(
        self, queue_item: QueueElement, action: Literal["add", "remove"] = "add"
    ):
        match action:
            case "add":
                self.run_queue.append(queue_item)
                self.table.add_row(queue_item)
                self.logger.info(f"Collection {queue_item} added to the queue")
            case "remove":
                # UH OH
                self.table.delete_row(queue_item)
                self.run_queue.remove(queue_item)
        self.logger.debug(f"Number of items in the queue: {len(self.run_queue)}")

    def clear_queue_table(self):
        while len(self.run_queue) > 0:
            _item_to_remove = self.run_queue[0]
            # delete row
            self.run_queue.popleft()
