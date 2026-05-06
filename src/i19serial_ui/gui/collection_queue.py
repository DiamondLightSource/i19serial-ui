from PyQt6 import QtWidgets


class CollectionQueueUI(QtWidgets.QTableWidget):
    """A table widget to display the queued collections and remove them as needed."""

    def __init__(self, rows, columns, parent):
        super().__init__(rows, columns, parent)
