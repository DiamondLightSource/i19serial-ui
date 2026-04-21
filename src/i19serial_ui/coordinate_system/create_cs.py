from i19serial_ui.log import LOGGER
from i19serial_ui.parameters.coordinates import Coord3D

ADJUST_FACTOR = 1e-9


def _get_delta(pos_1: Coord3D, pos_2: Coord3D) -> tuple[float, float, float]:
    _dx = pos_2.x - pos_1.x + ADJUST_FACTOR
    _dy = pos_2.y - pos_1.y + ADJUST_FACTOR
    _dz = pos_2.z - pos_1.z + ADJUST_FACTOR
    return (_dx, _dy, _dz)


def _get_step_size(delta: float, steps: int) -> float:
    return delta / (steps + 1)


def _get_well_index(h, v, tot):
    if v % 2:
        res = (tot - 1 - h) + (v * tot)
    else:
        res = h + (v * tot)
    return res


def make_coordinate_system(
    horizontal_wells: int,
    vertical_wells: int,
    fiducial_positions: tuple[Coord3D, Coord3D, Coord3D],
    decimals: int = 6,
) -> list[Coord3D]:
    delta_x_h, delta_y_h, delta_z_h = _get_delta(
        fiducial_positions[0], fiducial_positions[1]
    )
    delta_x_v, delta_y_v, delta_z_v = _get_delta(
        fiducial_positions[0], fiducial_positions[2]
    )
    step_x_h = _get_step_size(delta_x_h, horizontal_wells)
    step_y_h = _get_step_size(delta_y_h, horizontal_wells)
    step_z_h = _get_step_size(delta_z_h, horizontal_wells)
    step_x_v = _get_step_size(delta_x_v, vertical_wells)
    step_y_v = _get_step_size(delta_y_v, vertical_wells)
    step_z_v = _get_step_size(delta_z_v, vertical_wells)

    msg = f"""Delta and step sizes:
        horizontal delta_(x,y,z): {delta_x_h, delta_y_h, delta_z_h}
        vertical delta_(x,y,z): {delta_x_v, delta_y_v, delta_z_v}
        horizontal step sizes: {step_x_h, step_y_h, step_z_h}
        vertical step sizes: {step_x_v, step_y_v, step_z_v}
    """
    LOGGER.debug(msg)

    # Actual calculation
    _coord_list: list[Coord3D | None] = [
        None for _ in range(horizontal_wells * vertical_wells)
    ]
    _fid = fiducial_positions[0]

    for i in range(horizontal_wells):
        for j in range(vertical_wells):
            x = round(_fid.x + (i * step_x_h) + (j * step_x_v), decimals)
            y = round(_fid.y + (i * step_y_h) + (j * step_y_v), decimals)
            z = round(_fid.z + (i * step_z_h) + (j * step_z_v), decimals)

            if j % 2:  # Odd wells
                idx = (horizontal_wells - 1 - i) + (j * horizontal_wells)
            else:
                idx = i + (j * horizontal_wells)

            _coord_list[idx] = Coord3D(x, y, z)

    if not all(_coord_list):
        raise ValueError("")
    return _coord_list  # type: ignore
