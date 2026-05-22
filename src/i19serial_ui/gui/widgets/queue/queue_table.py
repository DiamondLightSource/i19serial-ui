from PyQt6 import QtWidgets
from PyQt6.QtCore import pyqtSignal, pyqtSlot

from i19serial_ui.parameters.queue import QueueElement

TABLE_LABELS = ["Remove", "Label", "Parameters"]
DELETE_BTN_STYLE = "QPushButton {color: red; font-weight: bold}"


class QueueTable(QtWidgets.QTableWidget):
    """A table widget to display the queued plans and remove them as needed."""

    deleted_collection = pyqtSignal(dict)

    def __init__(
        self,
        parent: QtWidgets.QWidget | None = None,
    ):
        super().__init__(parent)
        self.queue = []
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
        # btn.setIcon(QtGui.QIcon(image_file_path("delete.png")))
        btn.clicked.connect(lambda: self.delete_row(item_to_delete))
        return btn

    def _fill_in_table(self, item: QueueElement, row: int):
        self.setItem(row, 1, QtWidgets.QTableWidgetItem(item.element_label))
        # self.setItem(row, 1, QtWidgets.QTableWidgetItem(item.plan_name))
        self.setItem(row, 2, QtWidgets.QTableWidgetItem(str(item.plan_params)))  # FIXME

    @pyqtSlot
    def on_delete(self):
        pass

    def add_row(self, new_item: QueueElement):
        self.queue.append(new_item)
        num_rows = self.rowCount()
        # NOTE Assumption here is that it's only ever updated by one
        if len(self.queue) > num_rows:
            self.insertRow(num_rows)
            # First create the button
            _btn = self._create_delete_button(new_item)
            self.setCellWidget(num_rows, 0, _btn)
            # Then fill all the cells one by one, depending on collection type
            self._fill_in_table(new_item, num_rows)

    def delete_row(self, item_to_delete: QueueElement):
        pass
