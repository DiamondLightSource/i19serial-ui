from datetime import datetime
from enum import StrEnum
from importlib.resources import files
from pathlib import Path

from PyQt6.QtGui import QIcon

from i19serial_ui import assets, config

IMAGES_PATH = files(assets)
CONFIG_PATH = files(config)


class HutchInUse(StrEnum):
    EH1 = "EH1"
    EH2 = "EH2"


def image_file_path(filename: str, filepath: Path = IMAGES_PATH) -> str:  # type: ignore
    full_path = filepath.joinpath(filename)
    return full_path.as_posix()  # type: ignore


def config_file_path(hutch: HutchInUse, filepath: Path = CONFIG_PATH) -> Path:  # type: ignore
    match hutch:
        case HutchInUse.EH2:
            full_path = filepath.joinpath("i19_2_blueapi_config.yaml")
            return Path(full_path)  # type: ignore
        case HutchInUse.EH1:
            raise ValueError("No config file for EH1 yet")


def get_data_main_path() -> Path:
    year = datetime.now().year
    base_path = Path(f"/dls/i19-2/data/{year}")
    return base_path


def _create_image_icon(image_path: str) -> QIcon:
    icon = QIcon(image_path)
    return icon
