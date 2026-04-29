from collections.abc import Callable

from PyQt6 import QtCore, QtGui, QtWidgets

from i19serial_ui.blueapi_tools.blueapi_client import SerialBlueapiClient
from i19serial_ui.coordinate_system.create_cs import make_coordinate_system
from i19serial_ui.coordinate_system.utils import (
    _get_translated_coordinates,
    calculate_kapton_xz_positions,
    save_coordinates_to_json,
)
from i19serial_ui.gui.ui_utils import create_image_icon, image_file_path
from i19serial_ui.log import LOGGER
from i19serial_ui.parameters.coordinates import (
    COORD_FILE_PATH,
    Coord3D,
    Coordinates,
    FiducialPosition,
)
from i19serial_ui.parameters.grid import Grid, GridType

READ_POSITIONS_PLAN = "read_current_sample_stage_xyz_position"
MOVE_SAMPLE_STAGE_PLAN = "move_sample_stage"
TEST_CS_PLAN = "run_coordinate_system_test"


class CoordinateSystemPanel(QtWidgets.QWidget):
    def __init__(
        self,
        blueapi_client: SerialBlueapiClient,
        grid: Grid,
        parent: QtWidgets.QWidget | None = None,
    ):
        super().__init__(parent)
        self.client = blueapi_client
        self._grid = grid
        self.logger = LOGGER
        self.init_coordinates()
        self.init_buttons()
        self.init_text_boxes()
        self.cs_layout = self.create_layout()

    def create_layout(self):
        main_layout = QtWidgets.QVBoxLayout()
        positions_layout = self._setup_positions_layout()
        buttons_layout = self._setup_main_buttons_layout()
        main_layout.addLayout(positions_layout)
        main_layout.addLayout(buttons_layout)
        return main_layout

    def init_coordinates(self):
        self.coord_length = self._grid.size_x * self._grid.size_z
        self.coordinates: list[tuple] = []

    def init_buttons(self):
        self.make_btn = self._create_button(
            "Make coordinate system", self._make_coordinate_system
        )
        self.test_btn = self._create_button("Test", self._run_coordinate_system_test)
        self.clear_btn = self._create_button("Clear", self._clear_coordinates)
        self.save_btn = self._create_button("Save", self._save_coordinates)
        self.upload_btn = self._create_button("Upload", self._upload_coordinates)

    def init_text_boxes(self):
        self.top_left_x = QtWidgets.QLineEdit()
        self.top_left_y = QtWidgets.QLineEdit()
        self.top_left_z = QtWidgets.QLineEdit()
        self.top_right_x = QtWidgets.QLineEdit()
        self.top_right_y = QtWidgets.QLineEdit()
        self.top_right_z = QtWidgets.QLineEdit()
        self.bottom_left_x = QtWidgets.QLineEdit()
        self.bottom_left_y = QtWidgets.QLineEdit()
        self.bottom_left_z = QtWidgets.QLineEdit()

    def _fiducial_layout(
        self,
        position: FiducialPosition,
        icon_path: str,
        text_boxes: list[QtWidgets.QLineEdit],
    ):
        pos_layout = QtWidgets.QHBoxLayout()
        icon = create_image_icon(icon_path)
        icon_button = self._create_icon_button(
            icon,
            lambda: self.perform_grid_move(position),
        )
        btn = self._create_button(
            f"Set {position.value}",
            lambda: self._set_xyz_coordinates_for_fiducial(position, text_boxes),
        )
        btn.setFixedWidth(120)
        pos_layout.addWidget(icon_button)
        pos_layout.addWidget(btn)
        pos_layout.addWidget(text_boxes[0])
        pos_layout.addWidget(text_boxes[1])
        pos_layout.addWidget(text_boxes[2])
        return pos_layout

    def _set_xyz_coordinates_for_fiducial(
        self, position: FiducialPosition, text_boxes: list[QtWidgets.QLineEdit]
    ):
        self.logger.info(f"Setting x,y,z for position {position}")
        stage_positions = self.client.run_plan_and_get_result(READ_POSITIONS_PLAN, {})
        if not stage_positions:
            self.logger.error(
                "No positions could be read off the diffractometer, check blueapi logs"
            )
            return
        if self._grid.grid_type is GridType.KAPTON400:
            xz_offset = calculate_kapton_xz_positions(stage_positions[0:3:2], position)
            text_boxes[0].setText(str(xz_offset[0]))
            text_boxes[1].setText(str(stage_positions[1]))
            text_boxes[2].setText(str(xz_offset[1]))
        else:
            text_boxes[0].setText(str(stage_positions[0]))
            text_boxes[1].setText(str(stage_positions[1]))
            text_boxes[2].setText(str(stage_positions[2]))

    def _setup_positions_layout(self):
        layout = QtWidgets.QGridLayout()
        layout.addLayout(
            self._fiducial_layout(
                FiducialPosition.TL,
                image_file_path("TL.png"),
                [self.top_left_x, self.top_left_y, self.top_left_z],
            ),
            0,
            0,
        )
        layout.addLayout(
            self._fiducial_layout(
                FiducialPosition.TR,
                image_file_path("TR.png"),
                [self.top_right_x, self.top_right_y, self.top_right_z],
            ),
            1,
            0,
        )
        layout.addLayout(
            self._fiducial_layout(
                FiducialPosition.BL,
                image_file_path("BL.png"),
                [self.bottom_left_x, self.bottom_left_y, self.bottom_left_z],
            ),
            2,
            0,
        )
        return layout

    def _setup_main_buttons_layout(self):
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.make_btn)
        layout.addWidget(self.test_btn)
        layout.addWidget(self.clear_btn)
        layout.addWidget(self.save_btn)
        layout.addWidget(self.upload_btn)
        return layout

    def _create_button(
        self,
        name: str,
        func: Callable,
    ) -> QtWidgets.QPushButton:
        button = QtWidgets.QPushButton(name)
        button.clicked.connect(func)
        return button

    def _create_icon_button(
        self, icon: QtGui.QIcon, func: Callable
    ) -> QtWidgets.QPushButton:
        icon_button = QtWidgets.QPushButton("")
        icon_button.setIcon(icon)
        icon_button.setIconSize(QtCore.QSize(30, 30))
        icon_button.setFlat(True)
        icon_button.clicked.connect(func)
        return icon_button

    def _check_coordinates_text_fields(self, position: FiducialPosition) -> bool:
        if position == FiducialPosition.TL:
            if (
                self.top_left_x.text()
                and self.top_left_y.text()
                and self.top_left_z.text()
            ):
                return True
        if position == FiducialPosition.TR:
            if (
                self.top_right_x.text()
                and self.top_right_y.text()
                and self.top_right_z.text()
            ):
                return True
        if position == FiducialPosition.BL:
            if (
                self.bottom_left_x.text()
                and self.bottom_left_y.text()
                and self.bottom_left_z.text()
            ):
                return True
        return False

    def _read_coordinates_from_ui(self, position: FiducialPosition) -> Coord3D:
        try:
            if position == FiducialPosition.TL:
                _x = float(self.top_left_x.text())
                _y = float(self.top_left_y.text())
                _z = float(self.top_left_z.text())
            if position == FiducialPosition.TR:
                _x = float(self.top_right_x.text())
                _y = float(self.top_right_y.text())
                _z = float(self.top_right_z.text())
            if position == FiducialPosition.BL:
                _x = float(self.bottom_left_x.text())
                _y = float(self.bottom_left_y.text())
                _z = float(self.bottom_left_z.text())
        except ValueError:
            self.logger.error(
                f"""
                Can't read all coordinates for {position.value} position,
                are some fields blank?
                """
            )
            raise

        return Coord3D(_x, _y, _z)

    def _save_coordinates(self):
        try:
            self.logger.info("Saving coordinates to file")
            top_left = self._read_coordinates_from_ui(FiducialPosition.TL)
            top_right = self._read_coordinates_from_ui(FiducialPosition.TR)
            bottom_left = self._read_coordinates_from_ui(FiducialPosition.BL)
            coordinates = Coordinates(
                top_left=top_left,
                top_right=top_right,
                bottom_left=bottom_left,
            )
            self.logger.info(f"Coordinates: \n {coordinates}")

            save_coordinates_to_json("coordinates.json", coordinates)
        except Exception as e:
            self.logger.error("Unable to save coordinates")
            LOGGER.exception(e)

    def _upload_coordinates(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(
            None, directory=COORD_FILE_PATH.as_posix(), filter="Json file (*.json)"
        )[0]
        if not filename:
            self.logger.warning("No file selected")
            return
        self.logger.info(f"Uploading coordinates from file {filename}")
        try:
            coordinates = Coordinates.from_json(filename)
            self.top_left_x.setText(str(coordinates.top_left.x))
            self.top_left_y.setText(str(coordinates.top_left.y))
            self.top_left_z.setText(str(coordinates.top_left.z))
            self.top_right_x.setText(str(coordinates.top_right.x))
            self.top_right_y.setText(str(coordinates.top_right.y))
            self.top_right_z.setText(str(coordinates.top_right.z))
            self.bottom_left_x.setText(str(coordinates.bottom_left.x))
            self.bottom_left_y.setText(str(coordinates.bottom_left.y))
            self.bottom_left_z.setText(str(coordinates.bottom_left.z))
        except Exception:
            self.logger.error("Unable to upload coordinates")

    def _clear_coordinates(self):
        self.logger.info("Clear coordinates")
        text_boxes = [
            self.top_left_x,
            self.top_left_y,
            self.top_left_z,
            self.top_right_x,
            self.top_right_y,
            self.top_right_z,
            self.bottom_left_x,
            self.bottom_left_y,
            self.bottom_left_z,
        ]
        for box in text_boxes:
            box.setText("")

        self.init_coordinates()

    def _get_fiducial_coordinates_from_ui(
        self, position: FiducialPosition, other_fiducials: list[FiducialPosition]
    ) -> Coord3D:
        fid_1, fid_2 = other_fiducials
        if self._check_coordinates_text_fields(position):
            coords = self._read_coordinates_from_ui(position)
        elif self._check_coordinates_text_fields(fid_1):
            x1_y1_z1 = self._read_coordinates_from_ui(fid_1)
            dx_dy_dz = self._grid.get_fiducial_translation(position, fid_1)
            coords = _get_translated_coordinates(x1_y1_z1, dx_dy_dz)
        elif self._check_coordinates_text_fields(fid_2):
            x1_y1_z1 = self._read_coordinates_from_ui(fid_2)
            dx_dy_dz = self._grid.get_fiducial_translation(position, fid_2)
            coords = _get_translated_coordinates(x1_y1_z1, dx_dy_dz)
        else:
            raise ValueError("Can't read from UI, all fields appear to be empty")
        return coords

    def _work_out_fiducial_positions_from_text_input(self, position: FiducialPosition):
        match position:
            case FiducialPosition.TL:
                coords = self._get_fiducial_coordinates_from_ui(
                    position, [FiducialPosition.TR, FiducialPosition.BL]
                )
            case FiducialPosition.TR:
                coords = self._get_fiducial_coordinates_from_ui(
                    position, [FiducialPosition.TL, FiducialPosition.BL]
                )
            case FiducialPosition.BL:
                coords = self._get_fiducial_coordinates_from_ui(
                    position, [FiducialPosition.TL, FiducialPosition.TR]
                )

        return (coords.x, coords.y, coords.z)

    def _get_fiducial_positions_from_known_coordinates(
        self, position: FiducialPosition
    ) -> tuple[float, float, float]:
        _pos = self._grid.get_grid_positions()[position]
        coords = self.coordinates[_pos]
        self.logger.info(f"Moving to {coords}")
        return (coords[0], coords[1], coords[2])

    def perform_grid_move(self, position: FiducialPosition):
        """Move to the fiducial position by triggering a bluesky plan."""
        self.logger.info(f"Moving to grid position {position.value}")
        if len(self.coordinates) == 0:
            self.logger.info("Coordinate list not yet generated, using values from UI.")
            try:
                _x, _y, _z = self._work_out_fiducial_positions_from_text_input(position)
            except ValueError as err:
                self.logger.error(
                    "Error while reading coordinates, please type in some values!"
                )
                LOGGER.exception(err)
                return
            except Exception as e:
                self.logger.error(
                    "Something seems to be wrong with the input number format"
                )
                LOGGER.exception(e)
                return
        else:
            self.logger.info("Move fiducial from set coordinates")
            _x, _y, _z = self._get_fiducial_positions_from_known_coordinates(position)
        self.client.run_plan(MOVE_SAMPLE_STAGE_PLAN, {"coord": (_x, _y, _z)})

    def _make_coordinate_system(self):
        try:
            top_left = self._read_coordinates_from_ui(FiducialPosition.TL)
            top_right = self._read_coordinates_from_ui(FiducialPosition.TR)
            bottom_left = self._read_coordinates_from_ui(FiducialPosition.BL)

            fiducial_positions = (top_left, top_right, bottom_left)

            self.coordinates = make_coordinate_system(
                self._grid.size_x, self._grid.size_z, fiducial_positions
            )

        except Exception as e:
            self.logger.error("ERROR in creating the coordinates")
            LOGGER.exception(e)
            return

        self.logger.info(f"\t Coordinates: \n {self.coordinates}")
        if len(self.coordinates) != self.coord_length:
            self.logger.error("Coordinates may be missing, wrong length")
        self.logger.info(f"Coordinates len: {len(self.coordinates)}")

    def _run_coordinate_system_test(self):
        self.logger.info("Run a test to check on the coordinate system")
        if len(self.coordinates) == 0:
            self.logger.error("Please create the coordinate system first.")
            return
        self.client.run_plan(TEST_CS_PLAN, {"coord_list": self.coordinates})
