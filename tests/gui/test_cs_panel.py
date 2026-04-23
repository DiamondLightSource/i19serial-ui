from unittest.mock import patch

import pytest
from PyQt6 import QtWidgets

from i19serial_ui.gui.widgets.cs_panel import (
    CoordinateSystemPanel,
)
from i19serial_ui.parameters.coordinates import Coord3D, Coordinates, FiducialPosition
from i19serial_ui.parameters.grid import GridType

FAKE_COORDS = {
    "top_left": Coord3D(0.1, 0.0, 1.2),
    "top_right": Coord3D(0.1, 0.0, 1.4),
    "bottom_left": Coord3D(0.3, 0.0, 1.2),
}


@pytest.fixture
def mock_cs_panel(qtbot):
    with patch("i19serial_ui.gui.widgets.cs_panel.SerialBlueapiClient") as mock_client:
        test_panel = CoordinateSystemPanel(mock_client, GridType.POLYMER, (3, 3))
        qtbot.addWidget(test_panel)
        return test_panel


def set_values_to_all_boxes(mock_cs_panel):
    mock_cs_panel.top_left_x.setText("0.1")
    mock_cs_panel.top_left_y.setText("0.0")
    mock_cs_panel.top_left_z.setText("1.2")
    mock_cs_panel.top_right_x.setText("0.1")
    mock_cs_panel.top_right_y.setText("0.0")
    mock_cs_panel.top_right_z.setText("1.4")
    mock_cs_panel.bottom_left_x.setText("0.3")
    mock_cs_panel.bottom_left_y.setText("0.0")
    mock_cs_panel.bottom_left_z.setText("1.2")


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
    with (
        patch(
            "i19serial_ui.gui.widgets.cs_panel.Coordinates.from_json"
        ) as mock_json_load,
        patch(
            "i19serial_ui.gui.widgets.cs_panel.QtWidgets.QFileDialog.getOpenFileName"
        ) as patch_file,
    ):
        patch_file.return_value = "/chosen/path/to/coord.json"
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
    set_values_to_all_boxes(mock_cs_panel)

    mock_cs_panel._save_coordinates()

    mock_save.assert_called_once_with("coordinates.json", Coordinates(**FAKE_COORDS))


@patch("i19serial_ui.gui.widgets.cs_panel.save_coordinates_to_json")
def test_save_coordinates_does_not_run_if_value_missing(mock_save, mock_cs_panel):
    mock_cs_panel.top_right_x.setText("")

    mock_cs_panel._save_coordinates()

    mock_save.assert_not_called()


def test_check_coordinates_text_fields(mock_cs_panel):
    set_values_to_all_boxes(mock_cs_panel)

    for pos in [FiducialPosition.TL, FiducialPosition.TR, FiducialPosition.BL]:
        res = mock_cs_panel._check_coordinates_text_fields(pos)
        assert res


def test_check_coordinates_returns_false_if_one_box_empty(mock_cs_panel):
    mock_cs_panel.top_left_x.setText("1.0")
    mock_cs_panel.top_left_y.setText("0.5")
    mock_cs_panel.top_left_z.setText("")

    res = mock_cs_panel._check_coordinates_text_fields(FiducialPosition.TL)
    assert not res


def test_clear_coordinates_sets_all_boxes_to_empty_and_restes_coordinates_list(
    mock_cs_panel,
):
    text_boxes = [
        mock_cs_panel.top_left_x,
        mock_cs_panel.top_left_y,
        mock_cs_panel.top_left_z,
        mock_cs_panel.top_right_x,
        mock_cs_panel.top_right_y,
        mock_cs_panel.top_right_z,
        mock_cs_panel.bottom_left_x,
        mock_cs_panel.bottom_left_y,
        mock_cs_panel.bottom_left_z,
    ]
    set_values_to_all_boxes(mock_cs_panel)
    mock_cs_panel.coordinates = [(1, 1, 1), (2, 2, 2)]

    mock_cs_panel._clear_coordinates()

    assert mock_cs_panel.coordinates == []

    for box in text_boxes:
        assert box.text() == ""


def test_get_fiducial_coordinates_from_ui_raises_error_if_empty_values(mock_cs_panel):
    mock_cs_panel._clear_coordinates()
    with pytest.raises(ValueError):
        mock_cs_panel._get_fiducial_coordinates_from_ui(
            FiducialPosition.TL, [FiducialPosition.TR, FiducialPosition.BL]
        )


def test_get_fiducials_from_ui_reads_directly_if_text_fields_not_empty(mock_cs_panel):
    set_values_to_all_boxes(mock_cs_panel)

    coords = mock_cs_panel._get_fiducial_coordinates_from_ui(
        FiducialPosition.TR, [FiducialPosition.TL, FiducialPosition.BL]
    )

    assert coords == Coord3D(0.1, 0.0, 1.4)


@pytest.mark.parametrize(
    "position, other_positions, pos_used, check_fields",
    [
        (
            FiducialPosition.TR,
            [FiducialPosition.TL, FiducialPosition.BL],
            FiducialPosition.TL,
            (False, True, True),
        ),
        (
            FiducialPosition.TR,
            [FiducialPosition.TL, FiducialPosition.BL],
            FiducialPosition.BL,
            (False, False, True),
        ),
    ],
)
@patch("i19serial_ui.gui.widgets.cs_panel._get_translated_coordinates")
def test_get_fiducials_from_ui_works_out_value_from_correct_other_fiducial(
    mock_transl_coords,
    position,
    other_positions,
    pos_used,
    check_fields,
    mock_cs_panel,
):
    with (
        patch(
            "i19serial_ui.gui.widgets.cs_panel.CoordinateSystemPanel._check_coordinates_text_fields"
        ) as patch_check,
        patch(
            "i19serial_ui.gui.widgets.cs_panel.CoordinateSystemPanel._read_coordinates_from_ui"
        ) as patch_read,
    ):
        patch_check.side_effect = check_fields

        mock_cs_panel._get_fiducial_coordinates_from_ui(position, other_positions)

        patch_read.assert_called_once_with(pos_used)
        mock_transl_coords.assert_called_once()


@pytest.mark.parametrize(
    "pos, other_pos",
    [
        (FiducialPosition.TL, [FiducialPosition.TR, FiducialPosition.BL]),
        (FiducialPosition.TR, [FiducialPosition.TL, FiducialPosition.BL]),
        (FiducialPosition.BL, [FiducialPosition.TL, FiducialPosition.TR]),
    ],
)
def test_work_out_fiducial_position_from_ui(pos, other_pos, mock_cs_panel):
    with patch(
        "i19serial_ui.gui.widgets.cs_panel.CoordinateSystemPanel._get_fiducial_coordinates_from_ui"
    ) as patch_coords:
        mock_cs_panel._work_out_fiducial_positions_from_text_input(pos)
        patch_coords.assert_called_once_with(pos, other_pos)


def test_get_fiducial_from_known_coordinates(mock_cs_panel):
    mock_cs_panel.coordinates = [(0, 1, 2), (3, 4, 5)]

    coords = mock_cs_panel._get_fiducial_positions_from_known_coordinates(
        FiducialPosition.TL
    )

    assert coords == (0, 1, 2)


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


def test_set_xyz_coordinates_for_fiducial_when_using_kapton_grid(mock_cs_panel):
    mock_cs_panel._grid_type = GridType.KAPTON400
    mock_cs_panel.client.run_plan_and_get_result.return_value = (0.1, 0.0, 1.2)
    expected_positions = (0.250, 0.0, 1.05)

    text_boxes = [
        mock_cs_panel.top_left_x,
        mock_cs_panel.top_left_y,
        mock_cs_panel.top_left_z,
    ]

    mock_cs_panel._set_xyz_coordinates_for_fiducial(FiducialPosition.TL, text_boxes)

    assert float(mock_cs_panel.top_left_x.text()) == pytest.approx(
        expected_positions[0], 1e-2
    )
    assert float(mock_cs_panel.top_left_y.text()) == pytest.approx(
        expected_positions[1], 1e-2
    )
    assert float(mock_cs_panel.top_left_z.text()) == pytest.approx(
        expected_positions[2], 1e-2
    )


@pytest.mark.parametrize(
    "position, expected_coordinates",
    (
        [FiducialPosition.TL, (0.1, 0.0, 1.2)],
        [FiducialPosition.TR, (0.1, 0.0, 1.4)],
        [FiducialPosition.BL, (0.3, 0.0, 1.2)],
    ),
)
def test_perform_grid_move_from_ui_values(
    position, expected_coordinates, mock_cs_panel
):
    mock_cs_panel.coordinates = []
    set_values_to_all_boxes(mock_cs_panel)

    mock_cs_panel.perform_grid_move(position)

    mock_cs_panel.client.run_plan.assert_called_once_with(
        "move_sample_stage", {"coord": expected_coordinates}
    )


@pytest.mark.parametrize(
    "position, expected_coordinates",
    (
        [FiducialPosition.TL, (0.1, 0.0, 1.2)],
        [FiducialPosition.TR, (0.1, 0.0, 1.4)],
        [FiducialPosition.BL, (0.3, 0.0, 1.2)],
    ),
)
def test_perform_grid_move_from_coordinates(
    position, expected_coordinates, mock_cs_panel
):
    mock_cs_panel.coordinates = [(0.1, 0.0, 1.2), (0.1, 0.0, 1.4), (0.3, 0.0, 1.2)]
    with patch(
        "i19serial_ui.gui.widgets.cs_panel.CoordinateSystemPanel._get_fiducial_positions_from_known_coordinates"
    ) as patch_known_coords:
        patch_known_coords.return_value = expected_coordinates
        mock_cs_panel.perform_grid_move(position)

        mock_cs_panel.client.run_plan.assert_called_once_with(
            "move_sample_stage", {"coord": expected_coordinates}
        )


@patch("i19serial_ui.gui.widgets.cs_panel.make_coordinate_system")
def test_make_coordinate_system(mock_cs_maker, mock_cs_panel):
    set_values_to_all_boxes(mock_cs_panel)

    mock_cs_panel._make_coordinate_system()

    mock_cs_maker.assert_called_once_with(
        3, 3, ((0.1, 0.0, 1.2), (0.1, 0.0, 1.4), (0.3, 0.0, 1.2))
    )


def test_run_cs_test(mock_cs_panel):
    fake_coordinates = [(0, 0, 0), (0.1, 0.1, 0.1)]
    mock_cs_panel.coordinates = fake_coordinates

    mock_cs_panel._run_coordinate_system_test()

    mock_cs_panel.client.run_plan.assert_called_once_with(
        "run_coordinate_system_test", {"coord_list": fake_coordinates}
    )


def test_if_no_ccordinates_generated_test_does_not_run(mock_cs_panel):
    mock_cs_panel.coordinates = []

    mock_cs_panel._run_coordinate_system_test()

    mock_cs_panel.client.run_plan.assert_not_called()
