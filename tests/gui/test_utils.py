from pathlib import Path

import pytest
from PyQt6.QtGui import QIcon

from i19serial_ui.gui.ui_utils import (
    HutchInUse,
    _create_image_icon,
    config_file_path,
    get_data_main_path,
    image_file_path,
)


def test_create_icon():
    icon = _create_image_icon("")

    assert isinstance(icon, QIcon)


def test_get_data_main_path():
    res = get_data_main_path()

    assert res.as_posix() == "/dls/i19-2/data/2025"


def test_get_config_file_path_for_eh2():
    fake_path = Path("/some/path")
    config_path = config_file_path(HutchInUse.EH2, fake_path)

    assert config_path.as_posix() == "/some/path/i19_2_blueapi_config.yaml"


def test_get_image_file_path():
    img_path = image_file_path("image.png", Path("/some/path"))

    assert img_path == "/some/path/image.png"


def test_get_config_file_path_for_eh1_temporarily_raises_error():
    with pytest.raises(ValueError):
        config_file_path(HutchInUse.EH1, Path("/some/path"))
