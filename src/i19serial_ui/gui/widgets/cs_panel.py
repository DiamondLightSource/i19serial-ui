import json
from collections.abc import Callable
from pathlib import Path

from PyQt6 import QtCore, QtGui, QtWidgets

from i19serial_ui.blueapi_tools.blueapi_client import SerialBlueapiClient
from i19serial_ui.gui.ui_utils import create_image_icon, image_file_path
from i19serial_ui.log import LOGGER
from i19serial_ui.parameters.coordinates import (
    COORD_FILE_PATH,
    Coord3D,
    Coordinates,
    FiducialPosition,
)
from i19serial_ui.parameters.grid import Grid, GridType

READ_POSITIONS_PLAN_NAME = "read_current_sample_stage_xyz_position"

KAPTON_OFFSET = 0.150


def _calculate_kapton_xz_positions(
    xz: tuple[float, float], fiducial_position: FiducialPosition
) -> tuple[float, float]:
    match fiducial_position:
        case FiducialPosition.TL:
            return (xz[0] + KAPTON_OFFSET, xz[1] - KAPTON_OFFSET)
        case FiducialPosition.TR:
            return (xz[0] - KAPTON_OFFSET, xz[1] - KAPTON_OFFSET)
        case FiducialPosition.BL:
            return (xz[0] + KAPTON_OFFSET, xz[1] + KAPTON_OFFSET)


def placeholder_run_btn(s: str):
    LOGGER.info(s)


def save_coordinates_to_json(filename: Path | str, coordinates: Coordinates):
    full_filename = COORD_FILE_PATH / filename
    with open(full_filename, "w") as fh:
        json.dump(coordinates.model_dump(), fh, indent=4)


class CoordinateSystemPanel(QtWidgets.QWidget):
    coordinates: list[Coord3D | None]

    def __init__(
        self,
        blueapi_client: SerialBlueapiClient,
        grid_type: GridType,
        grid_size: tuple[int, int],  # xz
        parent: QtWidgets.QWidget | None = None,
    ):
        super().__init__(parent)
        self.client = blueapi_client
        self.grid_type = grid_type
        self.grid_size = grid_size
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
        coord_length = self.grid_size[0] * self.grid_size[1]
        self.coordinates = [None for _ in range(coord_length)]

    def init_buttons(self):
        self.make_btn = self._create_button(
            "Make coordinate system", lambda: placeholder_run_btn("CS MAKER")
        )
        self.test_btn = self._create_button(
            "Test", lambda: placeholder_run_btn("CS TEST")
        )
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
        LOGGER.info(f"Setting x,y,z for position {position}")
        stage_positions = self.client.run_plan_and_get_result(
            READ_POSITIONS_PLAN_NAME, {}
        )
        if not stage_positions:
            LOGGER.error(
                "No positions could be read off the diffractometer, check blueapi logs"
            )
            return
        if self.grid_type is GridType.KAPTON400:
            xz_offset = _calculate_kapton_xz_positions(stage_positions[0:3:2], position)
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

    def _update_xyz(self):
        pass

    def _save_coordinates(self):
        try:
            self.logger.info("Saving coordinates to file")
            top_left = (
                float(self.top_left_x.text()),
                float(self.top_left_y.text()),
                float(self.top_left_z.text()),
            )
            top_right = (
                float(self.top_right_x.text()),
                float(self.top_right_y.text()),
                float(self.top_left_z.text()),
            )
            bottom_left = (
                float(self.bottom_left_x.text()),
                float(self.bottom_left_y.text()),
                float(self.bottom_left_z.text()),
            )
            coordinates = Coordinates(
                top_left=Coord3D(*top_left),
                top_right=Coord3D(*top_right),
                bottom_left=Coord3D(*bottom_left),
            )
            self.logger.info(f"Coordinates: \n {coordinates}")

            save_coordinates_to_json("coordinates.json", coordinates)
        except Exception:
            self.logger.error("Unable to save coordinates")

    def _upload_coordinates(self):
        filename = COORD_FILE_PATH / "coordinates.json"
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

    def _work_out_fiducial_positions_from_text_input(self):
        coords = Coord3D(None, None, None)  # type: ignore
        if not all(coords):
            raise ValueError("Missing values in the input fields")
        return (coords.x, coords.y, coords.z)

    # THIS WHOLE LOGIC IS INSANE AND NEEDS RETHINKING.
    # THERE MUST BE A WAY OF SIMPLIFYING IT
    def perform_grid_move(self, position: FiducialPosition):
        """Plan will be:
        def move_grid_to_position([x,y,z], device_to_move) the device can be either
        newport or beamstop stage - will pass the name of the device here.
        Chosen from dropdown I guess.
        """
        LOGGER.info(f"Moving to grid position {position.value}")
        if not all(self.coordinates):  # all or some Nones
            LOGGER.info("Coordinate list not yet generated, using values from UI.")
            try:
                _x, _y, _z = self._work_out_fiducial_positions_from_text_input()
                self.client.run_plan(
                    "move_sample_stage_to_corners", {"corner_coord": (_x, _y, _z)}
                )
            except ValueError as err:
                LOGGER.error(
                    "Error while reading coordinates, please type in some values!"
                )
                LOGGER.exception(err)
            except Exception as e:
                LOGGER.error("Something seems to be wrong with the input number format")
                LOGGER.exception(e)
        else:
            LOGGER.info("Move fiducial from set coordinates")
            grid = Grid(*self.grid_size, self.grid_type)
            print(grid)
