import subprocess
import sys

from i19serial_ui import __version__


def test_cli_version():
    cmd = [sys.executable, "-m", "i19serial_ui", "--version"]
    assert subprocess.check_output(cmd).decode().strip() == __version__
