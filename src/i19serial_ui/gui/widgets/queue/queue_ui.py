from collections import deque

from PyQt6 import QtGui, QtWidgets
from PyQt6.QtCore import Qt, pyqtSlot

from i19serial_ui.gui.widgets.queue.queue_table import QueueTable
from i19serial_ui.log import LOGGER
from i19serial_ui.parameters.queue import QueueElement

QUEUE_WINDOW_SIZE = (800, 300)


class CollectionQueueUI(QtWidgets.QWidget):
    """A new window to handle/view to the queue."""

    def __init__(self):
        super().__init__()
        self.resize(*QUEUE_WINDOW_SIZE)
        self.setWindowTitle("Collection Queue")
        self.logger = LOGGER
        self.run_queue: deque[QueueElement] = deque()
        self.table = QueueTable(self.run_queue, self)
        self.table.remove_item_request.connect(self.on_delete_click)
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

    @pyqtSlot(QueueElement)
    def on_delete_click(self, queue_item: QueueElement):
        self.run_queue.remove(queue_item)
        self.logger.info(f"Number of items left in the queue: {len(self.run_queue)}")

    def add_to_queue_table(self, queue_item: QueueElement):
        self.run_queue.append(queue_item)
        self.table.add_row(queue_item)
        self.logger.info(f"{queue_item.element_label} added to the queue")
        self.logger.debug(f"Number of items in the queue: {len(self.run_queue)}")

    def clear_queue_table(self):
        while len(self.run_queue) > 0:
            _item_to_remove = self.run_queue[0]
            self.table.delete_row(_item_to_remove)
