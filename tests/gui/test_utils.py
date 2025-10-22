from PyQt6.QtGui import QIcon

from i19serial_ui.gui.ui_utils import _create_image_icon, get_data_main_path


def test_create_icon():
    icon = _create_image_icon("")

    assert isinstance(icon, QIcon)


def test_get_data_main_path():
    res = get_data_main_path()

    assert res.as_posix() == "/dls/i19-2/data/2025"
