import sys
from collections.abc import Callable
from pathlib import Path

from PyQt6 import QtCore, QtGui, QtWidgets

from i19serial_ui.blueapi_tools.blueapi_client import SerialBlueapiClient
from i19serial_ui.gui.ui_utils import (
    HutchInUse,
    config_file_path,
    create_image_icon,
    get_data_main_path,
    image_file_path,
)
from i19serial_ui.gui.widgets import (
    BacklightBox,
    GridOptions,
    InputPanel,
    LogBox,
    PhiAdjust,
    WellsSelectionPanel,
)
from i19serial_ui.gui.widgets.cs_panel import CoordinateSystemPanel
from i19serial_ui.log import (
    LOGGER,
    GuiWindowLogHandler,
    log_to_gui,
    tidy_up_logging,
)
from i19serial_ui.parameters.coordinates import FiducialPosition
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
        self.cs_panel = CoordinateSystemPanel(
            self.client,
            self.grid.current_grid,
            centralWidget,
        )

        self.phi_rotator = PhiAdjust(self.client, centralWidget)
        self.backlight = BacklightBox(self.client, centralWidget)
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
        self.toolbar.addAction(self.grid_move_tl_action)
        self.toolbar.addAction(self.grid_move_tr_action)
        self.toolbar.addAction(self.grid_move_bl_action)

    def _create_actions(self):
        self.select_visit_action = QtGui.QAction(self)
        self.select_visit_action.setIcon(
            create_image_icon(image_file_path("openDir.png"))
        )
        self.select_visit_action.triggered.connect(self.select_visit)
        self.home_action = QtGui.QAction(self)
        self.home_action.setIcon(create_image_icon(image_file_path("home.png")))
        self.run_action = QtGui.QAction(self)
        self.run_action.setIcon(create_image_icon(image_file_path("run.png")))
        self.run_action.triggered.connect(self.run)
        self.grid_move_tl_action = QtGui.QAction(self)
        self.grid_move_tl_action.setIcon(create_image_icon(image_file_path("TL.png")))
        self.grid_move_tl_action.triggered.connect(
            lambda: self.cs_panel.perform_grid_move(FiducialPosition.TL)
        )
        self.grid_move_tr_action = QtGui.QAction(self)
        self.grid_move_tr_action.setIcon(create_image_icon(image_file_path("TR.png")))
        self.grid_move_tr_action.triggered.connect(
            lambda: self.cs_panel.perform_grid_move(FiducialPosition.TR)
        )
        self.grid_move_bl_action = QtGui.QAction(self)
        self.grid_move_bl_action.setIcon(create_image_icon(image_file_path("BL.png")))
        self.grid_move_bl_action.triggered.connect(
            lambda: self.cs_panel.perform_grid_move(FiducialPosition.BL)
        )

    def _setup_title(self):
        self.i19_label = QtWidgets.QLabel("I19: Fixed Target Serial Crystallography")
        self.i19_label.setFont(QtGui.QFont(FONT, 13))
        self.i19_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def _create_dropdown(self):
        self.aperturedropdown = QtWidgets.QComboBox()
        self.aperturedropdown.addItems(list(ApertureOptions))
        self.selected_aperture = self.read_aperture_dropdown()

    def read_aperture_dropdown(self):
        return self.aperturedropdown.currentText()

    def _create_top_group(self):
        # move arrows, phi step, focuse, backlight etc
        self._create_dropdown()
        self.top_group = QtWidgets.QGroupBox()
        top_layout = QtWidgets.QGridLayout()

        self.ddb_label = QtWidgets.QLabel("Select aperture size:")
        self.ddb_label.setFont(QtGui.QFont(FONT, 10))
        self.ddb_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.aperturedropdown.setFixedWidth(100)

        left_layout = QtWidgets.QVBoxLayout()
        left_layout.addWidget(self.ddb_label)
        left_layout.addWidget(self.aperturedropdown)
        left_layout.setContentsMargins(12, 12, 12, 0)
        left_layout.addStretch()

        top_layout.addLayout(left_layout, 0, 0)
        top_layout.addLayout(self.backlight.backlight_layout, 0, 1)
        top_layout.addLayout(self.phi_rotator.phirotator_layout, 0, 2)
        self.top_group.setMaximumHeight(100)
        self.top_group.setLayout(top_layout)

    def _create_coordinate_system_group(self):
        self.cs_group = QtWidgets.QGroupBox("Coordinate System")
        self.cs_group.setLayout(self.cs_panel.cs_layout)

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

        self.run_btn = self._create_button("Run Plan", self.run)

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
        all_params = self.read_all_parameters()
        self.appendOutput("Start serial collection with the panda")
        self.appendOutput(f"With parameters: {all_params}")
        self.client.run_plan("run_serial_from_panda", all_params)

    def abort(self):
        self.client.abort_task()
        self.appendOutput("Abort")

    def read_wells(self):
        if self.wells.selection_checkbox.isChecked():
            well_list = self.wells.get_selected_wells_list()
            wells_chosen = {
                "first": well_list[0],
                "last": well_list[-1],
                "selected": well_list,
                "series_length": int(self.inputs.series_length.text()),
                "manual_selection_enabled": True,
            }
        else:
            wells_chosen = {
                "first": float(self.inputs.well_start.text()),
                "last": float(self.inputs.well_end.text()),
                "selected": range(1, int(self.inputs.well_end.text())),
                "series_length": int(self.inputs.series_length.text()),
                "manual_selection_enabled": False,
            }
        return wells_chosen

    def read_all_parameters(self):
        rotation_start = float(self.inputs.rotation_start.text())
        num_images = float(self.inputs.num_images.text())
        rotation_increment = float(self.inputs.image_width.text())
        rotation_end = rotation_start + num_images + rotation_increment
        detector_z = float(self.inputs.det_dist.text())
        detector_two_theta = float(self.inputs.two_theta.text())
        eh2_aperture = self.read_aperture_dropdown()

        params = {
            "parameters": {
                "detector_distance_mm": detector_z,
                "two_theta_deg": detector_two_theta,
                "rot_axis_start": rotation_start,
                "rot_axis_end": rotation_end,
                "rot_axis_increment": rotation_increment,
                "images_per_well": num_images,
                "exposure_time_s": float(self.inputs.time_image.text()),
                "aperture_request": eh2_aperture,
                "hutch": "EH2",
                "visit": Path(self.inputs.visit_path.text()),
                "dataset": self.inputs.dataset.text(),
                "filename_prefix": self.inputs.prefix.text(),
                "image_width_deg": float(self.inputs.image_width.text()),
                "transmission_fraction": float(self.inputs.transmission.text()),
                "grid": {
                    "grid_type": self.grid.grid_box.currentText(),
                    "x_steps": int(self.grid.grid_x.text()),
                    "z_steps": int(self.grid.grid_z.text()),
                },
                "detector_type": "EIGER",
                "well_position": {1: (1, 2, 3)},  # to be removed asap
                "wells": self.read_wells(),
            }
        }
        return params


def start_eh2_ui():
    app = QtWidgets.QApplication(sys.argv)
    main_window = SerialGuiEH2()
    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    start_eh2_ui()
