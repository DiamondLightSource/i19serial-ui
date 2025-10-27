import sys

from PyQt6 import QtCore, QtGui, QtWidgets

from i19serial_ui.gui.grid_options import GridOptions
from i19serial_ui.gui.input_panel import InputPanel
from i19serial_ui.gui.log_box import LogBox
from i19serial_ui.gui.ui_utils import (
    _create_image_icon,
    get_data_main_path,
    image_file_path,
)
from i19serial_ui.gui.wells_selection import WellsSelectionPanel
from i19serial_ui.log import (
    LOGGER,
    GuiWindowLogHandler,
    log_to_gui,
    tidy_up_logging,
)

WINDOW_SIZE = (600, 1200)
LOG_HANDLERS = []

# Some properties
BG_COLOUR = "background-colour:(133,194,132)"
FONT = "Arial"
BUTTON_STYLE = """background-colour:(133,194,132);
border-style:outset; border-width:2px;
border-radius:10px;
border-colour:black"""


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

        # Custom widgets
        self.log_widget = LogBox(centralWidget, self.LogHandler)
        self.inputs = InputPanel()
        self.wells = WellsSelectionPanel()
        self.grid = GridOptions()

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
        self._create_bottom_group()

        # General layout
        self.general_layout = self.create_main_layout()
        centralWidget.setLayout(self.general_layout)
        self.setCentralWidget(centralWidget)

        # Toolbar
        self._create_toolbar()

    def create_threads(self):
        pass

    def closeEvent(self, a0):  # type: ignore # noqa: N802
        self.gui_logger.debug("CLOSING UI")
        tidy_up_logging([self.gui_logger])  #  *LOGGERS])
        return super().closeEvent(a0)

    def _setup_logger(self):
        # setup_logging()
        self.gui_logger = LOGGER
        self.LogHandler = GuiWindowLogHandler()
        self.gui_logger.addHandler(self.LogHandler)
        # for logger in LOGGERS:
        #     logger.addHandler(self.LogHandler)

    def _create_toolbar(self):
        self.toolbar = QtWidgets.QToolBar(self)
        self.toolbar.setObjectName("toolbar")
        self.addToolBar(QtCore.Qt.ToolBarArea.LeftToolBarArea, self.toolbar)
        self._create_actions()
        self.toolbar.addAction(self.select_visit_action)
        self.toolbar.addAction(self.home_action)
        self.toolbar.addAction(self.run_action)

    def _create_actions(self):
        self.select_visit_action = QtGui.QAction(self)
        self.select_visit_action.setIcon(
            _create_image_icon(image_file_path("openDir.png"))
        )
        self.select_visit_action.triggered.connect(self.select_visit)
        self.home_action = QtGui.QAction(self)
        self.home_action.setIcon(_create_image_icon(image_file_path("home.png")))
        self.run_action = QtGui.QAction(self)
        self.run_action.setIcon(_create_image_icon(image_file_path("run.png")))
        self.run_action.triggered.connect(self.run)

    def _setup_title(self):
        self.i19_label = QtWidgets.QLabel("I19: Fixed Target Serial Crystallography")
        self.i19_label.setFont(QtGui.QFont(FONT, 13))
        self.i19_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def _create_top_group(self):
        # move arrows, phi step, focuse, backlight etc
        self.top_group = QtWidgets.QGroupBox()

    def _create_coordinate_system_group(self):
        self.cs_group = QtWidgets.QGroupBox("Coordinate System")

    def _create_collection_inputs_group(self):
        self.input_group = QtWidgets.QGroupBox("Collection set up")
        in_layout = QtWidgets.QVBoxLayout()
        in_layout.addLayout(self.inputs.inputs_layout)
        in_layout.addLayout(self.wells.selection_layout)
        in_layout.addLayout(self.grid.grid_layout)
        self.input_group.setLayout(in_layout)

    def _create_collection_buttons_group(self):
        self.run_btns_group = QtWidgets.QGroupBox()
        btn_layout = QtWidgets.QHBoxLayout()

        test_btn1 = QtWidgets.QPushButton("Run zebra")
        test_btn2 = QtWidgets.QPushButton("Run panda")
        test_btn3 = QtWidgets.QPushButton("Abort")

        test_btn1.clicked.connect(lambda: self.appendOutput("Run with zebra"))
        test_btn2.clicked.connect(lambda: self.appendOutput("Run with panda"))
        test_btn3.clicked.connect(lambda: self.appendOutput("Abort"))

        btn_layout.addWidget(test_btn1)
        btn_layout.addWidget(test_btn2)
        btn_layout.addWidget(test_btn3)

        self.run_btns_group.setLayout(btn_layout)

    def _create_bottom_group(self):
        # log panel view
        self.bottom_group = QtWidgets.QGroupBox()
        self.bottom_group.setLayout(self.log_widget.log_layout)

    def select_visit(self):
        base_path = get_data_main_path().as_posix()
        # NOTE. This works in venv but in dev container the base_path is not mounted
        # so it won't work.
        self.current_visit = QtWidgets.QFileDialog.getExistingDirectory(
            None,
            caption="Select visit",
            directory=base_path,
            options=QtWidgets.QFileDialog.Option.ShowDirsOnly,
        )
        if not self.current_visit:
            self.appendOutput("No visit selected, please try again!")
        else:
            self.appendOutput(f"Visit selected: {self.current_visit}")
            self.inputs.visit_path.setText(self.current_visit)

    def create_main_layout(self):
        title_layout = QtWidgets.QHBoxLayout()
        title_layout.addWidget(self.i19_label)
        main_layout = QtWidgets.QGridLayout()
        main_layout.addLayout(title_layout, 0, 0)
        main_layout.addWidget(self.top_group, 1, 0)
        main_layout.addWidget(self.cs_group, 2, 0)
        main_layout.addWidget(self.input_group, 3, 0)
        main_layout.addWidget(self.run_btns_group, 4, 0)
        main_layout.addWidget(self.bottom_group, 5, 0)
        return main_layout

    def appendOutput(self, msg: str, level: str = "INFO"):  # noqa: N802
        log_to_gui(self.gui_logger, msg, level)

    def run(self):
        self.appendOutput("RUN COLLECTION FROM HERE")


def start_eh2_ui():
    app = QtWidgets.QApplication(sys.argv)
    main_window = SerialGuiEH2()
    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    start_eh2_ui()
