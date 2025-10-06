from PyQt6.QtGui import QIcon

from i19serial_ui.gui.ui_utils import _create_image_icon


def test_create_icon():
    icon = _create_image_icon("")

    assert isinstance(icon, QIcon)
