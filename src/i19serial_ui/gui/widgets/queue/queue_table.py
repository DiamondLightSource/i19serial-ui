from collections import deque

from PyQt6 import QtWidgets
from PyQt6.QtCore import pyqtSignal

from i19serial_ui.log import LOGGER
from i19serial_ui.parameters.queue import QueueElement

TABLE_LABELS = ["Remove", "Label", "Parameters"]
DELETE_BTN_STYLE = "QPushButton {color: red; font-weight: bold}"


class QueueTable(QtWidgets.QTableWidget):
    """A table widget to display the queued plans and remove them as needed."""

    remove_item_request = pyqtSignal(QueueElement)

    def __init__(
        self,
        queue: deque[QueueElement],
        parent: QtWidgets.QWidget | None = None,
    ):
        super().__init__(parent)
        self.queue = queue
        self._setup_table()
        self.resize(740, 240)

    def _get_labels(self):
        self.table_labels = TABLE_LABELS

    def _setup_table(self):
        self._get_labels()
        self.setColumnCount(len(self.table_labels))
        self.setHorizontalHeaderLabels(self.table_labels)
        _header = self.horizontalHeader()
        _header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)  # type: ignore
        self.resizeColumnsToContents()

    def _create_delete_button(
        self, item_to_delete: QueueElement
    ) -> QtWidgets.QPushButton:
        btn = QtWidgets.QPushButton("X")
        btn.setStyleSheet(DELETE_BTN_STYLE)
        btn.clicked.connect(lambda: self.delete_row(item_to_delete))
        return btn

    def _fill_in_table(self, item: QueueElement, row: int):
        self.setItem(row, 1, QtWidgets.QTableWidgetItem(item.element_label))
        self.setItem(row, 2, QtWidgets.QTableWidgetItem(str(item.plan_params)))

    def add_row(self, new_item: QueueElement):
        num_rows = self.rowCount()
        # NOTE Assumption here is that it's only ever updated by one
        if len(self.queue) > num_rows:
            self.insertRow(num_rows)
            # First create the button
            _btn = self._create_delete_button(new_item)
            self.setCellWidget(num_rows, 0, _btn)
            # Then fill all the cells one by one, depending on collection type
            self._fill_in_table(new_item, num_rows)

    def _get_item_index_in_queue(self, id_to_delete: str):
        idx = [n for n, q in enumerate(self.queue) if q.id == id_to_delete]
        return idx[0]

    def delete_row(self, item_to_delete: QueueElement):
        idx = self._get_item_index_in_queue(item_to_delete.id)
        LOGGER.warning(f"Will delete item: {item_to_delete}, idx {idx}")
        self.removeRow(idx)
        self.remove_item_request.emit(item_to_delete)
