from pathlib import Path
from unittest.mock import patch

import pytest
from blueapi.config import ApplicationConfig

from i19serial_ui.blueapi_tools.blueapi_client import SerialBlueapiClient
from i19serial_ui.gui.widgets.cs_panel import CoordinateSystemPanel


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
    test_panel = CoordinateSystemPanel(mock_client, (3, 3))
    qtbot.addWidget(test_panel)
    return test_panel
