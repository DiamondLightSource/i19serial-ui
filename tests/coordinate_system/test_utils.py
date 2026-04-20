import pytest

from i19serial_ui.coordinate_system.utils import calculate_kapton_xz_positions
from i19serial_ui.parameters.coordinates import FiducialPosition


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
