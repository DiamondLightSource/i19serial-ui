from unittest.mock import patch

import pytest
from PyQt6 import QtWidgets

from i19serial_ui.gui.widgets.sample_focus import SampleFocus


@pytest.fixture
def mock_focus(qtbot):
    with patch("i19serial_ui.gui.widgets.cs_panel.SerialBlueapiClient") as mock_client:
        test_panel = SampleFocus(mock_client)
        qtbot.addWidget(test_panel)
        return test_panel


def test_focus_layout(mock_focus):
    assert mock_focus.focus_layout is not None
    assert isinstance(mock_focus.focus_layout, QtWidgets.QVBoxLayout)
    assert mock_focus.focus_layout.count() == 3

    btn_layout = mock_focus.focus_layout.children()[0]

    assert isinstance(btn_layout, QtWidgets.QHBoxLayout)


def test_click_small_focus_in_move(mock_focus):
    mock_focus.in_small.click()

    mock_focus.client.run_plan.assert_called_once_with(
        "move", {"moves": {"serial_stages.y": 0.005}}
    )


def test_click_large_focus_in_move(mock_focus):
    mock_focus.in_large.click()

    mock_focus.client.run_plan.assert_called_once_with(
        "move", {"moves": {"serial_stages.y": 0.05}}
    )


def test_click_small_focus_out_move(mock_focus):
    mock_focus.out_small.click()

    mock_focus.client.run_plan.assert_called_once_with(
        "move", {"moves": {"serial_stages.y": -0.005}}
    )


def test_click_large_focus_out_move(mock_focus):
    mock_focus.out_large.click()

    mock_focus.client.run_plan.assert_called_once_with(
        "move", {"moves": {"serial_stages.y": -0.05}}
    )
