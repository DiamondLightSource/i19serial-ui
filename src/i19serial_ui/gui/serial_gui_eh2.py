import sys
from collections.abc import Callable

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import pyqtSignal

from i19serial_ui.blueapi_tools.blueapi_client import SerialBlueapiClient
from i19serial_ui.blueapi_tools.blueapi_queue import BlueapiQueueRunner
from i19serial_ui.coordinate_system.utils import get_run_position_coordinates
from i19serial_ui.gui.ui_utils import (
    HutchInUse,
    config_file_path,
    create_image_icon,
    get_data_main_path,
    image_file_path,
    parse_dataset_input,
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
from i19serial_ui.gui.widgets.queue.queue_ui import RunQueueUI
from i19serial_ui.gui.widgets.sample_alignment import SampleAlignment
from i19serial_ui.gui.widgets.sample_focus import SampleFocus
from i19serial_ui.log import (
    LOGGER,
    GuiWindowLogHandler,
    log_to_gui,
    tidy_up_logging,
)
from i19serial_ui.parameters.coordinates import FiducialPosition
from i19serial_ui.parameters.general_utils import ApertureOptions
from i19serial_ui.parameters.queue import QueueElement
from i19serial_ui.parameters.wells_selection import WellsSelection

WINDOW_SIZE = (500, 1000)
LOG_HANDLERS = []


# Some properties
BG_COLOUR = "background-colour:(133,194,132)"
FONT = "Arial"
BUTTON_STYLE = """background-colour:(133,194,132);
border-style:outset; border-width:2px;
border-radius:10px;
border-colour:black"""


class SerialGuiEH2(QtWidgets.QMainWindow):
    selected_visit = pyqtSignal(str)
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
        self.focus = SampleFocus(self.client, centralWidget)
        self.sample_alignment = SampleAlignment(self.client, centralWidget)

        # External UI widgets
        self.queue_window = RunQueueUI()
        self.selected_visit.connect(self.queue_window.on_visit_update)
        self.run_queue = self.queue_window.run_queue

        # Thread for queue with polling
        self.queueThread = QtCore.QThread()

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

    def _setup_logger(self):
        self.gui_logger = LOGGER
        self.LogHandler = GuiWindowLogHandler()
        self.gui_logger.addHandler(self.LogHandler)

    def _setup_blueapi_client(self):
        self._config = config_file_path(self.hutch)
        self.client = SerialBlueapiClient(self._config)

    def closeEvent(self, a0):  # type: ignore # noqa: N802
        self.gui_logger.debug("CLOSING UI")
        if self.queue_window.isVisible():
            self.queue_window.close()
        tidy_up_logging([self.gui_logger])
        return super().closeEvent(a0)

    def open_queue_window(self):
        self.appendOutput("Opening queue window")
        self.queue_window.show()

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
        self.toolbar.addAction(self.open_queue_action)

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
        self.open_queue_action = QtGui.QAction(self)
        self.open_queue_action.setIcon(create_image_icon(image_file_path("queue.png")))
        self.open_queue_action.triggered.connect(self.open_queue_window)

    def _setup_title(self):
        self.i19_label = QtWidgets.QLabel("I19-2: Fixed Target Serial Crystallography")
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

        self.ddb_label = QtWidgets.QLabel("Select aperture:")
        self.ddb_label.setFont(QtGui.QFont(FONT, 10))
        self.ddb_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.aperturedropdown.setFixedWidth(70)

        left_layout = QtWidgets.QVBoxLayout()
        left_layout.addWidget(self.ddb_label)
        left_layout.addWidget(self.aperturedropdown)
        left_layout.setSpacing(10)
        left_layout.addStretch()

        top_layout.addLayout(self.sample_alignment.arrow_layout, 0, 0, 2, 2)
        top_layout.addLayout(self.phi_rotator.phirotator_layout, 0, 2, 1, 1)
        top_layout.addLayout(self.focus.focus_layout, 1, 2, 1, 1)
        top_layout.addLayout(self.backlight.backlight_layout, 0, 3, 1, 1)
        top_layout.addLayout(left_layout, 1, 3, 1, 1)
        self.top_group.setMaximumHeight(180)
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

        self.run_btn = self._create_button("Run", self.run)
        self.abort_btn = self._create_button("Abort", self.abort)
        self.queue_btn = self._create_button("Queue", self.add_to_queue)
        self.clear_btn = self._create_button("Clear Queue", self.clear_queue)

        btn_layout.addWidget(self.run_btn)
        btn_layout.addWidget(self.abort_btn)
        btn_layout.addWidget(self.queue_btn)
        btn_layout.addWidget(self.clear_btn)

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
            self.selected_visit.emit(self.current_visit)

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

    def _check_dataset_name_exists(self, dataset: str) -> bool:
        dset_exists: bool = False
        for item in self.run_queue:
            if item.plan_params["dataset"] == dataset:
                dset_exists = True
                break
        return dset_exists

    def add_to_queue(self):
        if not self.queue_window.isVisible():
            # If queue window not already visible, open it
            self.open_queue_window()
        try:
            new_collection = self.read_input_and_create_new_queue_element()
            if self._check_dataset_name_exists(new_collection.plan_params["dataset"]):
                self.gui_logger.warning(
                    f"""Collection not added to the queue:
                    dataset {new_collection.plan_params["dataset"]} already exists.
                    """
                )
                return
                # raise ValueError("Dataset already exists in the queue")
            self.queue_window.add_to_queue_table(new_collection)
            self.run_queue = self.queue_window.run_queue
            self.appendOutput("Collection added to the queue")
            self.appendOutput(f"QUEUE: \n {self.run_queue}")
        except Exception as e:
            self.appendOutput(
                "Couldn't add item to queue, please check logs.", level="ERROR"
            )
            self.gui_logger.exception(e)

    def clear_queue(self):
        self.appendOutput("Clearing the queue ...", level="WARNING")
        self.queue_window.clear_queue_table()
        self.run_queue = self.queue_window.run_queue
        self.appendOutput(f"Current queue: {self.run_queue}", level="DEBUG")

    def read_input_and_create_new_queue_element(self) -> QueueElement:
        parameters = self.read_all_parameters()
        if not parameters:
            self.appendOutput(
                "Please fill in all parameters before adding to the queue"
            )
            raise ValueError("Missing parameters")
        return QueueElement(
            plan_name="run_serial_from_panda",
            plan_params=parameters,
        )

    def finalise_collection_queue(self):
        self.run_queue = self.queue_window.run_queue
        if len(self.run_queue) == 0:
            new_collection = self.read_input_and_create_new_queue_element()
            self.run_queue.append(new_collection)

    def _run_single_task(self, queue_task: QueueElement):
        self.appendOutput(f"{queue_task.element_label}")
        self.appendOutput(f"With parameters: {queue_task.plan_params}")
        self.client.run_plan(
            queue_task.plan_name, {"parameters": queue_task.plan_params}
        )
        # TODO dev
        # self.appendOutput(
        #   f"With time: {queue_task.plan_params['exposure_time_s']} s"
        # )
        # self.client.run_plan(
        #     "sleep", {"time": queue_task.plan_params["exposure_time_s"]}
        # )

    def _set_up_queue_runner(self):
        self.queue_runner = BlueapiQueueRunner(self.client, self.run_queue)
        self.queue_runner.moveToThread(self.queueThread)
        self.queueThread.started.connect(self.queue_runner.start)
        self.queue_runner.finished.connect(self._on_run_end)
        self.queue_runner.task_done.connect(self.queue_window.table.clear_finished_task)

    def _on_run_end(self):
        self.queueThread.quit()
        self.queueThread.wait()
        # self.clear_queue()
        self.appendOutput("Run queue finished!")

    def run(self):
        try:
            self.finalise_collection_queue()
            if len(self.run_queue) == 1:
                task = self.run_queue.popleft()
                self._run_single_task(task)
                # Main issue here is that there is nothing
                # announcing end of collection yet.
            else:
                print("Run in thread")
                self._set_up_queue_runner()
                self.queueThread.start()
        except Exception as e:
            self.appendOutput(
                "There was an issue running the collection, please check logs"
            )
            self.gui_logger.exception(e)

    def abort(self):
        self.client.abort_task()
        self.appendOutput("Aborting collection and stoping queue if running.")
        if self.queueThread.isRunning():
            self.queue_runner.stop()

    def read_wells(self) -> WellsSelection:
        if self.wells.selection_checkbox.isChecked():
            well_list = self.wells.get_selected_wells_list()
            wells_chosen = {
                "first": int(well_list[0]),
                "last": int(well_list[-1]),
                "selected": well_list,
                "series_length": int(self.inputs.series_length.text()),
                "manual_selection_enabled": True,
            }
        else:
            wells_chosen = {
                "first": int(self.inputs.well_start.text()),
                "last": int(self.inputs.well_end.text()),
                "selected": list(range(1, int(self.inputs.well_end.text()) + 1)),
                "series_length": int(self.inputs.series_length.text()),
                "manual_selection_enabled": False,
            }

        return WellsSelection(**wells_chosen)

    def _get_collection_path(self) -> tuple[str, str, str]:
        visit = self.inputs.visit_path.text()
        dataset = self.inputs.dataset.text()
        prefix = self.inputs.prefix.text()
        _check = parse_dataset_input(visit, dataset, prefix)
        if not _check:
            self.appendOutput("Please check visit, dataset and prefix are all set.")
            raise ValueError("Visit, dataset or prefix not correctly set")
        return (visit, dataset, prefix)

    def read_all_parameters(self):
        params = {}
        _visit, _dataset, _prefix = self._get_collection_path()
        rotation_start = float(self.inputs.rotation_start.text())
        num_images = int(self.inputs.num_images.text())
        rotation_increment = float(self.inputs.image_width.text())
        rotation_end = rotation_start + num_images + rotation_increment
        detector_z = float(self.inputs.det_dist.text())
        detector_two_theta = float(self.inputs.two_theta.text())
        eh2_aperture = self.read_aperture_dropdown()
        wells = self.read_wells()

        params = {
            "detector_distance_mm": detector_z,
            "two_theta_deg": detector_two_theta,
            "rot_axis_start": rotation_start,
            "rot_axis_end": rotation_end,
            "rot_axis_increment": rotation_increment,
            "images_per_well": num_images,
            "exposure_time_s": float(self.inputs.time_image.text()),
            "aperture_request": eh2_aperture,
            "visit": _visit,  # Probably don't need
            "dataset": _dataset,
            "filename_prefix": _prefix,
            "image_width_deg": float(self.inputs.image_width.text()),
            "transmission_fraction": float(self.inputs.transmission.text()),
            "detector_type": "EIGER",
            "wells_to_collect": get_run_position_coordinates(
                wells, self.cs_panel.coordinates
            ),
            "wells_series_len": wells.series_length,
        }
        return params


def start_eh2_ui():
    app = QtWidgets.QApplication(sys.argv)
    main_window = SerialGuiEH2()
    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    start_eh2_ui()
