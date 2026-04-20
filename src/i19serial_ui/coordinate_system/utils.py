import json
from pathlib import Path

from i19serial_ui.parameters.coordinates import (
    COORD_FILE_PATH,
    Coordinates,
    FiducialPosition,
)

KAPTON_OFFSET = 0.150


def calculate_kapton_xz_positions(
    xz: tuple[float, float], fiducial_position: FiducialPosition
) -> tuple[float, float]:
    match fiducial_position:
        case FiducialPosition.TL:
            return (xz[0] + KAPTON_OFFSET, xz[1] - KAPTON_OFFSET)
        case FiducialPosition.TR:
            return (xz[0] - KAPTON_OFFSET, xz[1] - KAPTON_OFFSET)
        case FiducialPosition.BL:
            return (xz[0] + KAPTON_OFFSET, xz[1] + KAPTON_OFFSET)


def save_coordinates_to_json(filename: Path | str, coordinates: Coordinates):
    full_filename = COORD_FILE_PATH / filename
    with open(full_filename, "w") as fh:
        json.dump(coordinates.model_dump(), fh, indent=4)


def work_out_fiducial_positions_from_ui_input(
    fiducial: FiducialPosition,
) -> tuple[float, float, float]:
    return (0, 0, 0)
