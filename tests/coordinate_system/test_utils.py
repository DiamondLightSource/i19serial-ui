from unittest.mock import mock_open, patch

import pytest

from i19serial_ui.coordinate_system.utils import (
    _get_translated_coordinates,
    calculate_kapton_xz_positions,
    save_coordinates_to_json,
)
from i19serial_ui.parameters.coordinates import Coord3D, Coordinates, FiducialPosition


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
