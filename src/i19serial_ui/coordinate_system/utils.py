import json
from pathlib import Path

from i19serial_ui.parameters.coordinates import (
    COORD_FILE_PATH,
    Coord3D,
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


def save_coordinates_to_json(
    filename: Path | str,
    coordinates: Coordinates,
    filepath: Path | str = COORD_FILE_PATH,
):
    if not isinstance(filepath, Path):
        filepath = Path(filepath)
    full_filename = filepath / filename
    with open(full_filename, "w") as fh:
        json.dump(coordinates.model_dump(), fh, indent=4)


def _get_translated_coordinates(
    fiducial_coords: tuple[float, float, float],
    translation_vector: tuple[float, float, float],
) -> Coord3D:
    res = [(i + j) for i, j in zip(fiducial_coords, translation_vector, strict=True)]
    return Coord3D(*res)


def get_run_position_coordinates(
    self,
    wells_chosen: dict,
) -> dict[int, Coord3D]:
    # "Returns dict[int, Coord3D] (wellnum: position) for each well in series"
    run_positions: dict[int, Coord3D] = {}
    for well in wells_chosen["selected"]:
        _well_coords = self.coordinates[well - 1]
        run_positions[well] = _well_coords
    return run_positions
