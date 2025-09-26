import logging
import sys

from PyQt6 import QtCore, QtWidgets
from PyQt6.QtGui import QFont

from i19serial_ui.gui.log_box import LogBox
from i19serial_ui.log import GuiWindowLogHandler, tidy_up_logging

WINDOW_SIZE = (700, 1200)
LOG_HANDLERS = []

# Some properties
BG_COLOUR = "background-colour:(133,194,132)"
FONT = "Arial"
BUTTON_STYLE = """background-colour:(133,194,132);
border-style:outset; border-width:2px;
border-radius:10px;
border-colour:black"""


gui_logger = logging.getLogger("i19serial_ui.gui.eh2")


class SerialGuiEH2(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self._setup_logger()
        self.init_gui()

    def init_gui(self):
        _title = "Chemical Crystallography Serial GUI"
        self.setWindowTitle(_title)
        self.resize(*WINDOW_SIZE)
        self.setStyleSheet(BG_COLOUR)

        centralWidget = QtWidgets.QWidget(self)  # noqa: N806

        # Create boxes with layouts
        # Title
        self._setup_title()
        # Arrows, backlight, & co
        self._create_top_group()
        # Coordinate system
        self._create_coordinate_system_group()
        # Input
        self._create_collection_inputs_group()
        # Run buttons
        self._create_collection_buttons_group()
        # Log window
        self._create_bottom_group(centralWidget)

        # General layout
        self.general_layout = self.create_main_layout()
        centralWidget.setLayout(self.general_layout)
        self.setCentralWidget(centralWidget)

        # Toolbar
        # self._create_toolbar()

    def create_threads(self):
        pass

    def closeEvent(self, a0):  # type: ignore # noqa: N802
        return super().closeEvent(a0)

    def _setup_logger(self):
        self.gui_logger = gui_logger
        self.LogHandler = GuiWindowLogHandler()
        self.gui_logger.addHandler(self.LogHandler)
        # for logger in LOG_HANDLERS:
        #     logger.addHandler(self.LogHandler)

    def _create_toolbar(self):
        pass

    def _setup_title(self):
        self.i19_label = QtWidgets.QLabel("I19: Fixed Target Serial Crystallography")
        self.i19_label.setFont(QFont(FONT, 13))
        self.i19_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)

    def _create_top_group(self):
        # move arrows, phi step, focuse, backlight etc
        pass

    def _create_coordinate_system_group(self):
        pass

    def _create_collection_inputs_group(self):
        pass

    def _create_collection_buttons_group(self):
        pass

    def _create_bottom_group(self, centralWidget: QtWidgets.QWidget):  # noqa: N803
        # log panel view
        self.bottom_group = QtWidgets.QGroupBox()
        self.log_widget = LogBox(centralWidget, self.LogHandler)
        self.bottom_group.setLayout(self.log_widget.log_layout)

    def create_main_layout(self):
        title_layout = QtWidgets.QHBoxLayout()
        title_layout.addWidget(self.i19_label)
        main_layout = QtWidgets.QGridLayout()
        main_layout.addLayout(title_layout, 0, 0)
        main_layout.addWidget(self.bottom_group, 5, 0)
        return main_layout

    def appendOutput(self, msg: str, level: str = "INFO"):  # noqa: N802
        self.gui_logger.log(getattr(logging, level.upper()), f"{msg}")


def start_eh2_ui():
    app = QtWidgets.QApplication(sys.argv)
    main_window = SerialGuiEH2()
    main_window.show()
    sys.exit(app.exec())
    tidy_up_logging([gui_logger])


if __name__ == "__main__":
    start_eh2_ui()
