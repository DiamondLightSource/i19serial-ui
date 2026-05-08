import pytest

from i19serial_ui.parameters.coordinates import FiducialPosition
from i19serial_ui.parameters.grid import Grid, GridType


@pytest.mark.parametrize(
    "grid_type, expected_xz_step_size, expected_xz_block_size",
    [
        (GridType.POLYMER, (0.120, 0.120), (2.28, 2.28)),
        (GridType.SILICON, (0.125, 0.125), (2.375, 2.375)),
        (GridType.KAPTON400, (0.120, 0.120), (2.28, 2.28)),
        (GridType.FILM, (0.100, 0.100), (1.90, 1.90)),
    ],
)
def test_grid(
    grid_type: GridType,
    expected_xz_step_size: tuple[float, float],
    expected_xz_block_size: tuple[float, float],
):
    test_grid = Grid(20, 20, grid_type)

    assert test_grid.get_dim_xz_steps() == expected_xz_step_size
    assert test_grid.x_step_size == expected_xz_step_size[0]
    assert test_grid.z_step_size == expected_xz_step_size[1]
    assert test_grid.city_block_x == pytest.approx(expected_xz_block_size[0], 1e-2)
    assert test_grid.city_block_z == pytest.approx(expected_xz_block_size[1], 1e-2)


@pytest.mark.parametrize(
    "x, z, expected_pos",
    [
        (10, 10, [0, 9, 99, 89]),
        (5, 5, [0, 4, 19, 24]),
        (4, 2, [0, 3, 7, 3]),
        (4, 3, [0, 3, 7, 11]),
    ],
)
def test_get_grid_positions(x: int, z: int, expected_pos: list[float]):
    test_grid = Grid(x_steps=x, z_steps=z, grid_type=GridType.POLYMER)

    res = test_grid.get_grid_positions()

    assert res[FiducialPosition.TL] == expected_pos[0]
    assert res[FiducialPosition.TR] == expected_pos[1]
    assert res[FiducialPosition.BL] == expected_pos[2]


@pytest.mark.parametrize(
    "requested_fid, known_fid, grid_type, expected_vector",
    [
        (FiducialPosition.TL, FiducialPosition.TR, GridType.POLYMER, (-2.28, 0, 0)),
        (FiducialPosition.TL, FiducialPosition.BL, GridType.SILICON, (0, 0, 2.375)),
        (FiducialPosition.TR, FiducialPosition.BL, GridType.FILM, (1.90, 0, -1.90)),
        (
            FiducialPosition.BL,
            FiducialPosition.TR,
            GridType.KAPTON400,
            (-2.28, 0, -2.28),
        ),
        (FiducialPosition.BL, FiducialPosition.TL, GridType.POLYMER, (0, 0, -2.28)),
    ],
)
def test_fiducial_translation(
    requested_fid: FiducialPosition,
    known_fid: FiducialPosition,
    grid_type: GridType,
    expected_vector: tuple,
):
    test_grid = Grid(20, 20, grid_type)

    res = test_grid.get_fiducial_translation(requested_fid, known_fid)

    assert res[0] == pytest.approx(expected_vector[0], 1e-2)
    assert res[1] == pytest.approx(expected_vector[1], 1e-2)
    assert res[2] == pytest.approx(expected_vector[2], 1e-2)
