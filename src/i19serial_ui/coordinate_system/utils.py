import json
from pathlib import Path

from pydantic.dataclasses import dataclass

from i19serial_ui.log import LOGGER, log_to_gui
from i19serial_ui.parameters.coordinates import (
    COORD_FILE_PATH,
    Coord3D,
    Coordinates,
    FiducialPosition,
)

KAPTON_OFFSET = 0.150


@dataclass
class RunPositions:
    run_start: int
    run_end: int
    run_selection: list[int]


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


def get_run_positions(wells_chosen: dict, run_number: int) -> RunPositions:
    if wells_chosen["manual_selection_enabled"]:
        run_start = int(run_number * wells_chosen["series_length"])
        run_end = int((run_number + 1) * wells_chosen["series_length"] - 1)
        log_to_gui(LOGGER, f"Selected Wells: {wells_chosen['selected']}")
        log_to_gui(LOGGER, f"runListStart: {run_start}")
        log_to_gui(LOGGER, f"runListEnd: {run_end}")
        run_selection = (
            wells_chosen["selected"][run_start:]
            if run_end - run_start > len(wells_chosen["selected"])
            else wells_chosen["selected"][run_start : run_end + 1]
        )
        log_to_gui(LOGGER, f"runSelectedWells: {run_selection}")
    else:
        # Ensures we go from the first position at run start to the final position
        # at run end
        run_start = int(
            run_number * wells_chosen["series_length"] + wells_chosen["first"]
        )
        run_end = int(
            (run_number + 1) * wells_chosen["series_length"] - 1 + wells_chosen["first"]
        )
        log_to_gui(LOGGER, f"Selected Wells: {wells_chosen['selected']}")
        log_to_gui(LOGGER, f"runListStart: {run_start}")
        log_to_gui(LOGGER, f"runListEnd: {run_end}")
        # FIXME There must be a better way, too tired to think of it now
        run_selection = (
            [*range(run_start, len(wells_chosen["selected"]) + 1)]
            if run_end - run_start > len(wells_chosen["selected"])
            else [*range(run_start, run_end + 1)]
        )
        log_to_gui(LOGGER, f"runSelectedWells: {run_selection}")
    return RunPositions(
        run_start=run_start, run_end=run_end, run_selection=run_selection
    )


def get_run_position_coordinates(
    wells_chosen: dict,
    run_number: int,
    # num_images: int, was in the code before but doesn't seem to be used?
    coordinates: list[tuple],
) -> dict[int, tuple]:
    # "Returns dict[int, tuple] (wellnum: position) for each well in series"
    # I know we said string/tuple, but int/tuple
    log_to_gui(LOGGER, f"Starting {run_number} of {wells_chosen['selected']}")
    _positions = get_run_positions(wells_chosen, run_number)

    # run_length = len(_positions.run_selection)  also unsure why this is here.
    run_positions: dict[int, tuple] = {}
    for well in _positions.run_selection:
        _well_coords = coordinates[well - 1]
        run_positions[well] = _well_coords
    return run_positions
