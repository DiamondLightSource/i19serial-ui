import subprocess
import sys
from unittest.mock import MagicMock, patch

from i19serial_ui import __version__
from i19serial_ui.__main__ import main


def test_cli_version():
    cmd = [sys.executable, "-m", "i19serial_ui", "--version"]
    assert (
        subprocess.check_output(cmd).decode().strip() == f"I19 serial UI v{__version__}"
    )


@patch("i19serial_ui.__main__.start_eh2_ui")
def test_main_cli_opens_correct_ui_for_eh2(mock_start_ui: MagicMock):
    main(["2"])

    mock_start_ui.assert_called_once()


@patch("i19serial_ui.__main__.start_eh2_ui")
def test_main_cli_for_eh1_ui_not_opened(mock_start_ui: MagicMock):
    main(["1"])

    mock_start_ui.assert_not_called()
