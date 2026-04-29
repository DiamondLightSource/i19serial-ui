from unittest.mock import mock_open, patch

import pytest

from i19serial_ui.coordinate_system.create_cs import (
    make_coordinate_system,
)
from i19serial_ui.coordinate_system.utils import (
    RunPositions,
    _get_translated_coordinates,
    calculate_kapton_xz_positions,
    get_run_position_coordinates,
    get_run_positions,
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
                1: (0.0, 0.0, 0.0),
                10: (0.4736842105263158, 0.0, 0.0),  # will fix when we round to 3
                20: (0.9999999999999999, 0.0, 0.0),
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
                1: (0.0, 0.0, 0.0),
                2: (0.05263157894736842, 0.0, 0.0),  # will fix when we round to 3
                3: (0.10526315789473684, 0.0, 0.0),
                4: (0.15789473684210525, 0.0, 0.0),
                5: (0.21052631578947367, 0.0, 0.0),
            },
        ),
    ],
)
def test_get_run_position_coordinates(wells_chosen, run_positions, results):
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
                "selected": [1, 10, 20, 30, 40, 50],
                "series_length": 3,
                "manual_selection_enabled": True,
            },
            0,  # first 3
            {
                "run_start": 0,
                "run_end": 2,
                "run_selection": [1, 10, 20],
            },
        ),
        (
            {
                "first": 1,
                "last": 20,
                "selected": [1, 10, 20, 30, 40, 50],
                "series_length": 3,
                "manual_selection_enabled": True,
            },
            1,  # second 3
            {
                "run_start": 3,
                "run_end": 5,
                "run_selection": [30, 40, 50],
            },
        ),
        (
            {
                "first": 1,
                "last": 10,
                "selected": list(range(1, 10)),
                "series_length": 5,
                "manual_selection_enabled": False,
            },
            0,  # first 5
            {
                "run_start": 1,
                "run_end": 5,
                "run_selection": list(range(1, 6)),
            },
        ),
        (
            {
                "first": 1,
                "last": 5,
                "selected": list(range(1, 10)),
                "series_length": 5,
                "manual_selection_enabled": False,
            },
            1,  # second 5
            {
                "run_start": 1,
                "run_end": 5,
                "run_selection": list(range(6, 10)),
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
