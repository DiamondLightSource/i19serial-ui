from scanspec.core import Path as ScanPath
from scanspec.specs import Line

from i19serial_ui.parameters.coordinates import Coord3D


def _calculate_spec_points(
    pos_1: Coord3D,
    pos_2: Coord3D,
    horizontal_wells: int,
    vertical_wells: int,
):
    # Beacause "flipped" when mounted -> z is horizontal
    spec = Line("z", pos_1.z, pos_2.z, horizontal_wells) * ~Line(
        "x", pos_1.x, pos_2.x, vertical_wells
    )
    scan_path = ScanPath(spec.calculate())
    points = scan_path.consume().midpoints
    return points


def make_coordinate_system(
    horizontal_wells: int,
    vertical_wells: int,
    fiducial_positions: tuple[Coord3D, Coord3D, Coord3D],
) -> list[tuple]:
    grid_points = _calculate_spec_points(
        fiducial_positions[0], fiducial_positions[2], horizontal_wells, vertical_wells
    )
    y_pos = fiducial_positions[0].y  # This one doesn't change

    coord_list = []
    for i, j in zip(grid_points["x"], grid_points["z"], strict=False):
        _c = (float(i), y_pos, float(j))
        coord_list.append(_c)
    return coord_list
