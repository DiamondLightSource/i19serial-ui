import argparse
import subprocess
import sys
from unittest.mock import MagicMock, patch

from i19serial_ui import __version__


def test_cli_version():
    cmd = [sys.executable, "-m", "i19serial_ui", "--version"]
    assert (
        subprocess.check_output(cmd).decode().strip() == f"I19 serial UI v{__version__}"
    )


def _parse_input(val: int):
    parser = argparse.ArgumentParser(description=f"Open eh{val} UI")  # noqa: F841


@patch("i19serial_ui.__main__.start_eh2_ui")
def test_cli_opens_correct_cli_for_eh2(mock_start_ui: MagicMock):
    pass
