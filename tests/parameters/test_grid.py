import pytest

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

    assert test_grid.dim_xz_steps == expected_xz_step_size
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
    test_grid = Grid(x, z, GridType.POLYMER)

    res = test_grid.get_grid_positions()

    assert res["top_left"] == expected_pos[0] and res["top_right"] == expected_pos[1]
    assert (
        res["bottom_left"] == expected_pos[2] and res["bottom_right"] == expected_pos[3]
    )
