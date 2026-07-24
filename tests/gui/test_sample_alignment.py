from unittest.mock import patch

import pytest
from PyQt6 import QtWidgets

from i19serial_ui.gui.widgets.sample_alignment import NudgeDirection, SampleAlignment


@pytest.fixture
def mock_align(qtbot):
    with patch(
        "i19serial_ui.gui.widgets.sample_alignment.SerialBlueapiClient"
    ) as mock_client:
        test_panel = SampleAlignment(mock_client)
        qtbot.addWidget(test_panel)
        return test_panel


def test_alignment_layout(mock_align):
    assert mock_align.arrow_layout is not None
    assert isinstance(mock_align.arrow_layout, QtWidgets.QGridLayout)
    assert mock_align.arrow_layout.count() == 9

    assert isinstance(mock_align.up_small, QtWidgets.QPushButton)


def test_click_small_up_move(mock_align):
    expected_motor = "serial_stages.z"
    expected_distance = 0.002

    mock_align.up_small.click()

    mock_align.client.run_plan.assert_called_once_with(
        "move", {"moves": {expected_motor: expected_distance}}
    )


def test_click_large_up_move(mock_align):
    expected_motor = "serial_stages.z"
    expected_distance = 0.01

    mock_align.up_large.click()

    mock_align.client.run_plan.assert_called_once_with(
        "move", {"moves": {expected_motor: expected_distance}}
    )


def test_click_small_down_move(mock_align):
    expected_motor = "serial_stages.z"
    expected_distance = -0.002

    mock_align.down_small.click()

    mock_align.client.run_plan.assert_called_once_with(
        "move", {"moves": {expected_motor: expected_distance}}
    )


def test_click_large_down_move(mock_align):
    expected_motor = "serial_stages.z"
    expected_distance = -0.01

    mock_align.down_large.click()

    mock_align.client.run_plan.assert_called_once_with(
        "move", {"moves": {expected_motor: expected_distance}}
    )


def test_click_small_left_move(mock_align):
    expected_motor = "serial_stages.x"
    expected_distance = -0.002

    mock_align.left_small.click()

    mock_align.client.run_plan.assert_called_once_with(
        "move", {"moves": {expected_motor: expected_distance}}
    )


def test_click_large_left_move(mock_align):
    expected_motor = "serial_stages.x"
    expected_distance = -0.01

    mock_align.left_large.click()

    mock_align.client.run_plan.assert_called_once_with(
        "move", {"moves": {expected_motor: expected_distance}}
    )


def test_click_small_right_move(mock_align):
    expected_motor = "serial_stages.x"
    expected_distance = 0.002

    mock_align.right_small.click()

    mock_align.client.run_plan.assert_called_once_with(
        "move", {"moves": {expected_motor: expected_distance}}
    )


def test_click_large_right_move(mock_align):
    expected_motor = "serial_stages.x"
    expected_distance = 0.01

    mock_align.right_large.click()

    mock_align.client.run_plan.assert_called_once_with(
        "move", {"moves": {expected_motor: expected_distance}}
    )


@pytest.mark.parametrize(
    "nudge_direction, expected_motor",
    [(NudgeDirection.X, "serial_stages.x"), (NudgeDirection.Z, "serial_stages.z")],
)
def test_on_click_run_move_plan(
    nudge_direction: NudgeDirection, expected_motor: str, mock_align
):
    mock_align._on_click_run_move_plan(0.1, nudge_direction)

    mock_align.client.run_plan.assert_called_once_with(
        "move", {"moves": {expected_motor: 0.1}}
    )
