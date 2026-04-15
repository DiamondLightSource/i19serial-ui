from pathlib import Path
from unittest.mock import patch

import pytest
from blueapi.config import ApplicationConfig
from PyQt6 import QtWidgets

from i19serial_ui.blueapi_tools.blueapi_client import SerialBlueapiClient
from i19serial_ui.gui.widgets.cs_panel import CoordinateSystemPanel
from i19serial_ui.parameters.grid import GridType


@pytest.fixture
def mock_client() -> SerialBlueapiClient:
    with patch(
        "i19serial_ui.blueapi_tools.blueapi_client.SerialBlueapiClient._load_config_from_file"
    ) as patch_config:
        patch_config.return_value = ApplicationConfig()
        client = SerialBlueapiClient(Path("/some/config.yaml"))
    return client


@pytest.fixture
def mock_cs_panel(mock_client, qtbot):
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
