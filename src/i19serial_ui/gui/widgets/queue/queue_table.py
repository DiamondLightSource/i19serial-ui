from PyQt6 import QtWidgets

from i19serial_ui.parameters.queue import QueueElement

TABLE_LABELS = ["Remove", "Label", "Parameters"]
DELETE_BTN_STYLE = "QPushButton {color: red; font-weight: bold}"


class QueueTable(QtWidgets.QTableWidget):
    """A table widget to display the queued plans and remove them as needed."""

    def __init__(
        self,
        parent: QtWidgets.QWidget | None = None,
    ):
        super().__init__(parent)
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

    def create_delete_button(
        self,
    ) -> QtWidgets.QPushButton:
        btn = QtWidgets.QPushButton("X")
        btn.setStyleSheet(DELETE_BTN_STYLE)
        return btn

    def fill_in_table(self, item: QueueElement, row: int):
        self.setItem(row, 1, QtWidgets.QTableWidgetItem(item.element_label))
        self.setItem(row, 2, QtWidgets.QTableWidgetItem(str(item.plan_params)))

    def clear_finished_task(self, idx: int):
        # Just needs to clear the table row
        # No need to delete from the queue because it should have already been removed
        self.removeRow(idx)
