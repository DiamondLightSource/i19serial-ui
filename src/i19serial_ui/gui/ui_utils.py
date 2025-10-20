from datetime import datetime
from importlib.resources import files
from pathlib import Path

from PyQt6.QtGui import QIcon

from i19serial_ui import assets

IMAGES_PATH = files(assets)


def image_file_path(filename: str) -> str:
    full_path = IMAGES_PATH.joinpath(filename)
    return full_path.as_posix()  # type: ignore


def get_data_main_path() -> Path:
    year = datetime.now().year
    base_path = Path(f"/dls/i19-2/data/{year}")
    return base_path


def _create_image_icon(image_path: str) -> QIcon:
    icon = QIcon(image_path)
    return icon
