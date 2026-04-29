from unittest.mock import patch

import numpy as np
import pytest
from numpy.testing import assert_array_equal

from i19serial_ui.coordinate_system.create_cs import (
    _calculate_spec_points,
    make_coordinate_system,
)
from i19serial_ui.coordinate_system.utils import (
    RunPositions,
    get_run_position_coordinates,
    get_run_positions,
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


@pytest.mark.parametrize(
    "wells_chosen,results,run_positions",
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
                1: (0.0, 0.0, 0.0),
                10: (0.4736842105263158, 0.0, 0.0),  # will fix when we round to 3
                20: (0.9999999999999999, 0.0, 0.0),
            },
            {
                "run_start": 1,  # 1+1 * 1-1
                "run_end": 20,  # 2*20 -1
                "run_selection": [1, 10, 20],
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
                1: (0.0, 0.0, 0.0),
                2: (0.05263157894736842, 0.0, 0.0),  # will fix when we round to 3
                3: (0.10526315789473684, 0.0, 0.0),
                4: (0.15789473684210525, 0.0, 0.0),
                5: (0.21052631578947367, 0.0, 0.0),
            },
            {
                "run_start": 1,
                "run_end": 5,
                "run_selection": [1, 2, 3, 4, 5],
            },
        ),
    ],
)
def test_get_run_position_coordinates(wells_chosen, results, run_positions):
    with patch(
        "i19serial_ui.coordinate_system.utils.get_run_positions",
        return_value=RunPositions(
            run_start=run_positions["run_start"],
            run_end=run_positions["run_end"],
            run_selection=run_positions["run_selection"],
        ),
    ):
        fiducials = (Coord3D(0, 0, 0), Coord3D(1, 0, 0), Coord3D(0, 0, 1))
        coordinates = make_coordinate_system(20, 20, fiducials)
        assert get_run_position_coordinates(wells_chosen, 0, coordinates) == results
        # I think this just tests the positions correctly?


@pytest.mark.parametrize(
    "wells_chosen,run_number,result",
    [
        (
            {
                "first": 1,
                "last": 20,
                "selected": [1, 10, 20],
                "series_length": 3,
                "manual_selection_enabled": True,
            },
            0,
            {
                "run_start": 0,
                "run_end": 2,
                "run_selection": [1, 10, 20],
            },
        ),
        (
            {
                "first": 1,
                "last": 5,
                "selected": list(range(1, 6)),
                "series_length": 1,
                "manual_selection_enabled": False,
            },
            0,
            {
                "run_start": 1,
                "run_end": 5,
                "run_selection": [1, 2, 3, 4, 5],
            },
        ),
    ],
)
def test_get_run_positions(wells_chosen, run_number, result):
    run_pos = get_run_positions(wells_chosen, run_number)
    if wells_chosen["manual_selection_enabled"]:
        assert run_pos.run_start == result["run_start"]
        assert run_pos.run_end == result["run_end"]
        assert run_pos.run_selection == result["run_selection"]
