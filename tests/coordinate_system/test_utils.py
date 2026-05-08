from unittest.mock import mock_open, patch

import pytest

from i19serial_ui.coordinate_system.create_cs import (
    make_coordinate_system,
)
from i19serial_ui.coordinate_system.utils import (
    _get_translated_coordinates,
    calculate_kapton_xz_positions,
    get_run_position_coordinates,
    save_coordinates_to_json,
)
from i19serial_ui.parameters.coordinates import Coord3D, Coordinates, FiducialPosition
from i19serial_ui.parameters.wells_selection import WellsSelection


@pytest.mark.parametrize(
    "fiducial, xz, expected_xz",
    [
        (FiducialPosition.TL, (0.2, 1.0), (0.350, 0.850)),
        (FiducialPosition.TR, (0.2, 1.0), (0.050, 0.850)),
        (FiducialPosition.BL, (0.2, 1.0), (0.350, 1.150)),
    ],
)
def test_calculate_kapton_xz_positions(fiducial, xz, expected_xz):
    res = calculate_kapton_xz_positions(xz, fiducial)

    assert res[0] == pytest.approx(expected_xz[0], 1e-3)
    assert res[1] == pytest.approx(expected_xz[1], 1e-3)


def test_get_translated_coordinates():
    expected_coordinates = (-0.5, 0.0, 4.375)
    res = _get_translated_coordinates((-0.5, 0.0, 2), (0, 0, 2.375))

    assert res == Coord3D(*expected_coordinates)


def test_save_coordinates_to_json():
    coord = Coordinates(
        top_right=Coord3D(0, 0, 1),
        top_left=Coord3D(0, 0, 0),
        bottom_left=Coord3D(1, 0, 0),
    )
    with (
        patch("i19serial_ui.coordinate_system.utils.open", mock_open()),
        patch("i19serial_ui.coordinate_system.utils.json.dump") as patch_dump,
    ):
        save_coordinates_to_json("coord.json", coord, "/some/path")
        patch_dump.assert_called_once()


@pytest.mark.parametrize(
    "wells_chosen,run_positions,results",
    [
        (
            {
                "first": 1,
                "last": 20,
                "selected": [1, 10, 20],
                "series_length": 3,
                "manual_selection_enabled": True,
            },
            {
                "run_start": 1,
                "run_end": 20,
                "run_selection": [1, 10, 20],
            },
            {
                "1": (0.0, 0.0, 0.0),
                "10": (0.4736842105263158, 0.0, 0.0),  # will fix when we round to 3
                "20": (0.9999999999999999, 0.0, 0.0),
            },
        ),
        (
            {
                "first": 1,
                "last": 5,
                "selected": list(range(1, 6)),
                "series_length": 6,
                "manual_selection_enabled": False,
            },
            {
                "run_start": 1,
                "run_end": 5,
                "run_selection": [1, 2, 3, 4, 5],
            },
            {
                "1": (0.0, 0.0, 0.0),
                "2": (0.05263157894736842, 0.0, 0.0),  # will fix when we round to 3
                "3": (0.10526315789473684, 0.0, 0.0),
                "4": (0.15789473684210525, 0.0, 0.0),
                "5": (0.21052631578947367, 0.0, 0.0),
            },
        ),
    ],
)
def test_get_run_position_coordinates(wells_chosen, results):
    fidcials = (Coord3D(0, 0, 0), Coord3D(1, 0, 0), Coord3D(0, 0, 1))
    coordinates = make_coordinate_system(20, 20, fidcials)
    wells_chosen = WellsSelection(**wells_chosen)
    assert get_run_position_coordinates(wells_chosen, coordinates) == results
