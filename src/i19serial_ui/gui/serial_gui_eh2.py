import sys
from collections.abc import Callable

from PyQt6 import QtCore, QtGui, QtWidgets

from i19serial_ui.blueapi_tools.blueapi_client import SerialBlueapiClient
from i19serial_ui.gui.ui_utils import (
    HutchInUse,
    _create_image_icon,
    config_file_path,
    get_data_main_path,
    image_file_path,
)
from i19serial_ui.gui.widgets import (
    GridOptions,
    InputPanel,
    LogBox,
    WellsSelectionPanel,
)
from i19serial_ui.log import (
    LOGGER,
    GuiWindowLogHandler,
    log_to_gui,
    tidy_up_logging,
)
from i19serial_ui.parameters.general_utils import ApertureOptions

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
    hutch: HutchInUse = HutchInUse.EH2

    def __init__(self) -> None:
        super().__init__()
        self._setup_logger()
        self._setup_blueapi_client()
        self.init_gui()

    def init_gui(self):
        _title = "Chemical Crystallography Serial GUI"
        self.setWindowTitle(_title)
        self.resize(*WINDOW_SIZE)
        self.setStyleSheet(BG_COLOUR)

        centralWidget = QtWidgets.QWidget(self)  # noqa: N806

        # Custom widgets
        self.log_widget = LogBox(centralWidget, self.LogHandler)
        self.inputs = InputPanel(centralWidget)
        self.wells = WellsSelectionPanel(centralWidget)
        self.grid = GridOptions(centralWidget)

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
        self.gui_logger = LOGGER
        self.LogHandler = GuiWindowLogHandler()
        self.gui_logger.addHandler(self.LogHandler)
        # for logger in LOGGERS:
        #     logger.addHandler(self.LogHandler)

    def _setup_blueapi_client(self):
        self._config = config_file_path(self.hutch)
        self.client = SerialBlueapiClient(self._config)

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

    def _create_dropdown(self):
        self.aperturedropdown = QtWidgets.QComboBox()
        self.aperturedropdown.addItems(list(ApertureOptions))
        self.selected_aperture = self.read_aperture_dropdown()

    def _create_adjuster(self):
        self.phiadjusterpositive = self._create_button(
            "+", self.on_click_move_phi_deg_pos
        )
        self.phiadjusternegative = self._create_button(
            "-", self.on_click_move_phi_deg_neg
        )
        self.phianglebox = QtWidgets.QLineEdit()

    def read_aperture_dropdown(self):
        return self.aperturedropdown.currentText()

    def _create_top_group(self):
        # move arrows, phi step, focuse, backlight etc
        self._create_dropdown()
        self.top_group = QtWidgets.QGroupBox()
        top_layout = QtWidgets.QGridLayout()
        self.ddb_label = QtWidgets.QLabel("Select aperture size:")
        self.ddb_label.setFont(QtGui.QFont(FONT, 10))
        self.ddb_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.adj_label = QtWidgets.QLabel("Phi")
        self.adj_label.setFont(QtGui.QFont(FONT, 10))
        self.adj_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.aperturedropdown.setFixedWidth(150)
        self._create_adjuster()
        self.phianglebox.setText("25")
        self.top_group.setLayout(top_layout)

        top_layout.setColumnStretch(3, 2)
        left_layout = QtWidgets.QHBoxLayout()

        left_layout.addWidget(self.ddb_label)
        left_layout.addWidget(self.aperturedropdown)

        right_layout = QtWidgets.QHBoxLayout()
        right_layout.addWidget(self.adj_label)
        right_layout.addWidget(self.phiadjusterpositive)
        right_layout.addWidget(self.phianglebox)
        right_layout.addWidget(self.phiadjusternegative)

        top_layout.addLayout(left_layout, 0, 0)
        top_layout.addLayout(right_layout, 0, 1)
        top_layout.setColumnStretch(0, 1)

    def _create_coordinate_system_group(self):
        self.cs_group = QtWidgets.QGroupBox("Coordinate System")

    def _create_collection_inputs_group(self):
        self.input_group = QtWidgets.QGroupBox("Collection set up")
        in_layout = QtWidgets.QVBoxLayout()
        in_layout.addLayout(self.inputs.inputs_layout)
        in_layout.addLayout(self.wells.selection_layout)
        in_layout.addLayout(self.grid.grid_layout)
        self.input_group.setLayout(in_layout)

    def _create_button(
        self,
        name: str,
        func: Callable,
    ) -> QtWidgets.QPushButton:
        button = QtWidgets.QPushButton(name)
        button.clicked.connect(func)
        return button

    def _create_collection_buttons_group(self):
        self.run_btns_group = QtWidgets.QGroupBox()
        btn_layout = QtWidgets.QHBoxLayout()

        self.run_btn = self._create_button("Run Plan", self.run_serial)

        self.abort_btn = self._create_button("Abort", self.abort)

        btn_layout.addWidget(self.run_btn)
        btn_layout.addWidget(self.abort_btn)

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
            _session = self.current_visit.split("/")[-1]
            self.client.update_session(_session)

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

    def abort(self):
        self.client.abort_task()
        self.appendOutput("Abort")

    def run_serial(self):
        rotation_start = float(self.inputs.rotation_start.text())
        num_images = float(self.inputs.num_images.text())
        rotation_increment = float(self.inputs.image_width.text())
        rotation_end = rotation_start + num_images + rotation_increment
        detector_z = float(self.inputs.det_dist.text())
        detector_two_theta = float(self.inputs.two_theta.text())
        eh2_aperture = self.read_aperture_dropdown()
        params = {
            "detector_distance_mm": detector_z,
            "two_theta_deg": detector_two_theta,
            "rot_axis_start": rotation_start,
            "rot_axis_end": rotation_end,
            "rot_axis_increment": rotation_increment,
            "images_per_well": num_images,
            "exposure_time_s": float(self.inputs.time_image.text()),
            "aperture_request": eh2_aperture,
        }
        #     "hutch": "EH2",
        #     "visit": "/tmp/i19-2/cm12345-1",
        #     "dataset": "foo",
        #     "filename_prefix": "bar_01",
        #     "image_width_deg": 0.1,
        #     "transmission_fraction": 0.3,
        #     "grid": {
        #         "grid_type": "Silicon",
        #         "x_steps": 20,
        #         "z_steps": 20,
        #     },
        #     "detector_type": "EIGER",
        #     "well_position": {1: (1, 2, 3)},
        #     "wells": dummy_wells_settings,
        self.client.run_plan("run_serial_from_panda", params)
        self.appendOutput("Start serial collection with the panda")
        self.appendOutput(f"With parameters: {params}")

    def on_click_move_phi_deg_pos(self):
        rotation_start = float(self.inputs.rotation_start.text())
        rotation_increment = float(self.phianglebox.text())
        rotation_end = rotation_start + rotation_increment
        params = {
            "rot_axis_start": rotation_start,
            "rot_axis_end": rotation_end,
            "rot_axis_increment": rotation_increment,
        }
        self.client.run_plan("rotate_in_phi", params)
        self.appendOutput("Start serial collection with the panda")
        self.appendOutput(f"With parameters: {params}")

    def on_click_move_phi_deg_neg(self):
        rotation_start = float(self.inputs.rotation_start.text())
        rotation_increment = -float(self.phianglebox.text())
        rotation_end = rotation_start + rotation_increment
        params = {
            "rot_axis_start": rotation_start,
            "rot_axis_end": rotation_end,
            "rot_axis_increment": rotation_increment,
        }
        self.client.run_plan("rotate_in_phi", params)
        self.appendOutput("Start serial collection with the panda")
        self.appendOutput(f"With parameters: {params}")


def start_eh2_ui():
    app = QtWidgets.QApplication(sys.argv)
    main_window = SerialGuiEH2()
    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    start_eh2_ui()
