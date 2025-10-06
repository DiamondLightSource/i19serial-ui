from PyQt6 import QtWidgets

from i19serial_ui.log import GuiWindowLogHandler

GREETING = "Hello crystallographer, let's do some science."


class LogBox(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget, handler: GuiWindowLogHandler):
        super().__init__(parent)
        self._parent = parent
        self.log_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.log_layout)
        self.handler = handler
        self.init_log()

    def init_log(self):
        self.log_output_box = QtWidgets.QPlainTextEdit(self._parent)
        self.log_output_box.appendPlainText(GREETING)
        self.log_output_box.setReadOnly(True)
        self.handler.signalLog.connect(self.log_output_box.appendPlainText)
        self.log_layout.addWidget(self.log_output_box)
