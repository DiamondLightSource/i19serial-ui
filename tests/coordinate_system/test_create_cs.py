import numpy as np
import pytest
from numpy.testing import assert_array_equal

from i19serial_ui.coordinate_system.create_cs import (
    _calculate_spec_points,
    make_coordinate_system,
)
from i19serial_ui.parameters.coordinates import Coord3D


def test_calculate_spec_points():
    expected_z = np.repeat([0, 2.5, 5], 3)
    expected_x = np.array([0, 2.5, 5, 5, 2.5, 0, 0, 2.5, 5])
    p = _calculate_spec_points(
        Coord3D(0, 0, 0), Coord3D(5, 0, 0), Coord3D(0, 0, 5), 3, 3
    )

    assert "x" in p.keys() and "z" in p.keys()
    assert len(p["x"]) == len(p["z"])

    assert_array_equal(p["z"], expected_z)
    assert_array_equal(p["x"], expected_x)


@pytest.mark.parametrize(
    "h_wells, v_wells, expected_list",
    [
        (2, 2, [(0.0, 0, 0.0), (1.0, 0, 0.0), (1.0, 0, 1.0), (0.0, 0, 1.0)]),
        (
            3,
            3,
            [
                (0.0, 0, 0.0),
                (0.5, 0, 0.0),
                (1.0, 0, 0.0),
                (1.0, 0, 0.5),
                (0.5, 0, 0.5),
                (0.0, 0, 0.5),
                (0.0, 0, 1.0),
                (0.5, 0, 1.0),
                (1.0, 0, 1.0),
            ],
        ),
        (
            3,
            2,
            [
                (0.0, 0, 0.0),
                (1.0, 0, 0.0),
                (1.0, 0, 0.5),
                (0.0, 0, 0.5),
                (0.0, 0, 1.0),
                (1.0, 0, 1.0),
            ],
        ),
        (1, 3, [(0.0, 0, 0.0), (0.5, 0, 0.0), (1.0, 0, 0.0)]),
    ],
)
def test_make_coordinate_system_returns_correct_list(h_wells, v_wells, expected_list):
    fiducials = (Coord3D(0, 0, 0), Coord3D(1, 0, 0), Coord3D(0, 0, 1))

    coordinates = make_coordinate_system(h_wells, v_wells, fiducials)

    assert coordinates == expected_list
