from unittest.mock import patch

import pytest
from PyQt6 import QtWidgets

from i19serial_ui.gui.widgets.cs_panel import (
    CoordinateSystemPanel,
    _calculate_kapton_xz_positions,
)
from i19serial_ui.parameters.coordinates import Coord3D, Coordinates, FiducialPosition
from i19serial_ui.parameters.grid import GridType

FAKE_COORDS = {
    "top_left": Coord3D(0.1, 0.0, 1.2),
    "top_right": Coord3D(0.1, 0.0, 1.4),
    "bottom_left": Coord3D(0.3, 0.0, 1.2),
}


@pytest.mark.parametrize(
    "fiducial, xz, expected_xz",
    [
        (FiducialPosition.TL, (0.2, 1.0), (0.350, 0.850)),
        (FiducialPosition.TR, (0.2, 1.0), (0.050, 0.850)),
        (FiducialPosition.BL, (0.2, 1.0), (0.350, 1.150)),
    ],
)
def test_calculate_kapton_xz_positions(fiducial, xz, expected_xz):
    res = _calculate_kapton_xz_positions(xz, fiducial)

    assert res[0] == pytest.approx(expected_xz[0], 1e-3)
    assert res[1] == pytest.approx(expected_xz[1], 1e-3)


@pytest.fixture
def mock_cs_panel(qtbot):
    with patch("i19serial_ui.gui.widgets.cs_panel.SerialBlueapiClient") as mock_client:
        test_panel = CoordinateSystemPanel(mock_client, GridType.POLYMER, (3, 3))
        qtbot.addWidget(test_panel)
        return test_panel


def test_cs_panel_layout(mock_cs_panel):
    assert mock_cs_panel.cs_layout is not None
    assert isinstance(mock_cs_panel.cs_layout, QtWidgets.QVBoxLayout)
    assert mock_cs_panel.cs_layout.count() == 2

    (pos_layout, btn_layout) = mock_cs_panel.cs_layout.children()

    assert isinstance(pos_layout, QtWidgets.QGridLayout)
    assert isinstance(btn_layout, QtWidgets.QHBoxLayout)


def test_coordinates_text_fields_update_when_uploaded_from_json(mock_cs_panel):
    expected_top_left = (0.1, 0.0, 1.2)
    expected_top_right = (0.1, 0.0, 1.4)
    expected_bottom_left = (0.3, 0.0, 1.2)
    with patch(
        "i19serial_ui.gui.widgets.cs_panel.Coordinates.from_json"
    ) as mock_json_load:
        mock_json_load.return_value = Coordinates(**FAKE_COORDS)
        mock_cs_panel._upload_coordinates()

        assert mock_cs_panel.top_left_x.text() == str(expected_top_left[0])
        assert mock_cs_panel.top_left_y.text() == str(expected_top_left[1])
        assert mock_cs_panel.top_left_z.text() == str(expected_top_left[2])
        assert mock_cs_panel.top_right_x.text() == str(expected_top_right[0])
        assert mock_cs_panel.top_right_y.text() == str(expected_top_right[1])
        assert mock_cs_panel.top_right_z.text() == str(expected_top_right[2])
        assert mock_cs_panel.bottom_left_x.text() == str(expected_bottom_left[0])
        assert mock_cs_panel.bottom_left_y.text() == str(expected_bottom_left[1])
        assert mock_cs_panel.bottom_left_z.text() == str(expected_bottom_left[2])


@patch("i19serial_ui.gui.widgets.cs_panel.save_coordinates_to_json")
def test_save_coordinates(mock_save, mock_cs_panel):
    mock_cs_panel.top_left_x.setText("0.1")
    mock_cs_panel.top_left_y.setText("0.0")
    mock_cs_panel.top_left_z.setText("1.2")
    mock_cs_panel.top_right_x.setText("0.1")
    mock_cs_panel.top_right_y.setText("0.0")
    mock_cs_panel.top_right_z.setText("1.4")
    mock_cs_panel.bottom_left_x.setText("0.3")
    mock_cs_panel.bottom_left_y.setText("0.0")
    mock_cs_panel.bottom_left_z.setText("1.2")

    mock_cs_panel._save_coordinates()

    mock_save.assert_called_once_with("coordinates.json", Coordinates(**FAKE_COORDS))


@patch("i19serial_ui.gui.widgets.cs_panel.save_coordinates_to_json")
def test_save_coordinates_does_not_run_if_value_missing(mock_save, mock_cs_panel):
    mock_cs_panel.top_right_x.setText("")

    mock_cs_panel._save_coordinates()

    mock_save.assert_not_called()


@pytest.mark.parametrize(
    "fiducial, positions",
    [
        (FiducialPosition.TL, (0.1, 0.0, 1.2)),
        (FiducialPosition.TR, (0.1, 0.0, 1.4)),
        (FiducialPosition.BL, (0.3, 0.0, 1.2)),
    ],
)
def test_set_xyz_coordinates_for_fiducial(fiducial, positions, mock_cs_panel):
    mock_cs_panel.client.run_plan_and_get_result.return_value = positions

    if fiducial == FiducialPosition.TL:
        text_boxes = [
            mock_cs_panel.top_left_x,
            mock_cs_panel.top_left_y,
            mock_cs_panel.top_left_z,
        ]
    elif fiducial == FiducialPosition.TR:
        text_boxes = [
            mock_cs_panel.top_right_x,
            mock_cs_panel.top_right_y,
            mock_cs_panel.top_right_z,
        ]
    else:
        text_boxes = [
            mock_cs_panel.bottom_left_x,
            mock_cs_panel.bottom_left_y,
            mock_cs_panel.bottom_left_z,
        ]

    mock_cs_panel._set_xyz_coordinates_for_fiducial(fiducial, text_boxes)

    assert text_boxes[0].text() == str(positions[0])
    assert text_boxes[1].text() == str(positions[1])
    assert text_boxes[2].text() == str(positions[2])
