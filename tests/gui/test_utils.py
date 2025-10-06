from pathlib import Path

from PyQt6.QtGui import QIcon

from i19serial_ui.gui.ui_utils import _create_image_icon, image_file_path


def test_image_file_path():
    assets_path = Path(__file__).parents[2]
    print(assets_path)
    img = image_file_path("test.png")

    assert img == f"{assets_path.as_posix()}/src/i19serial_ui/assets/test.png"


def test_create_icon():
    icon = _create_image_icon("")

    assert isinstance(icon, QIcon)
