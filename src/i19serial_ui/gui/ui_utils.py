from importlib.resources import files

from PyQt6.QtGui import QIcon

from i19serial_ui import assets

IMAGES_PATH = files(assets)


def image_file_path(filename: str) -> str:
    full_path = IMAGES_PATH.joinpath(filename)
    return full_path.as_posix()  # type: ignore


def _create_image_icon(image_path: str) -> QIcon:
    icon = QIcon(image_path)
    return icon
