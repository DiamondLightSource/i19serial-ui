from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, call, patch

import pytest
from PyQt6.QtGui import QIcon

from i19serial_ui.gui.ui_utils import (
    HutchInUse,
    config_file_path,
    create_image_icon,
    get_data_main_path,
    image_file_path,
    parse_dataset_input,
)


def test_create_icon():
    icon = create_image_icon("")

    assert isinstance(icon, QIcon)


def test_get_data_main_path():
    year = datetime.now().year
    res = get_data_main_path()

    assert res.as_posix() == f"/dls/i19-2/data/{year}"


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


@pytest.mark.parametrize(
    "dataset, prefix, check_result",
    [("", "filename", False), ("test", "", False), ("test", "new_file", True)],
)
def test_parse_dataset_info(dataset: str, prefix: str, check_result: bool):
    fake_visit = "/path/to/cm12345-1"

    res = parse_dataset_input(fake_visit, dataset, prefix)
    assert res == check_result


@patch("i19serial_ui.gui.ui_utils.LOGGER")
@patch("i19serial_ui.gui.ui_utils.log_to_gui")
@patch("i19serial_ui.gui.ui_utils.os.path.isdir")
def test_parse_dataset_info_returns_false_when_directory_exists(
    mock_isdir: MagicMock, mock_log: MagicMock, mock_logger: MagicMock
):
    mock_isdir.return_value = True
    expected_err_msg = (
        "Data collection folder already exsists, please choose unique name"
    )

    res = parse_dataset_input("/some/path", "test", "file")
    assert not res
    mock_log.assert_has_calls(
        [
            call(mock_logger, "Checking input information", level="DEBUG"),
            call(mock_logger, expected_err_msg, level="ERROR"),
        ]
    )
