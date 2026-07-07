import os
from datetime import datetime
from enum import StrEnum
from importlib.resources import files
from pathlib import Path

from PyQt6.QtGui import QIcon

from i19serial_ui import assets, config
from i19serial_ui.log import LOGGER, log_to_gui

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


def create_image_icon(image_path: str) -> QIcon:
    icon = QIcon(image_path)
    return icon


def check_input_information(
    visit: str, dataset: str | None, prefix: str | None
) -> bool:
    """Check that dataset and prefix have been passed and are unique."""
    # NOTE visit check is handled by the instrument session
    # NOTE Numtracker will take care to check access to visit, but for now...
    log_to_gui(LOGGER, "Checking input information", level="DEBUG")
    if not dataset:
        log_to_gui(
            LOGGER,
            "Dataset has not been set, please provide a dataset name",
            level="ERROR",
        )
        return False
    if not prefix:
        log_to_gui(
            LOGGER,
            "Prefix has not been set, please provide a prefix name",
            level="ERROR",
        )
        return False
    if os.path.isdir(f"{visit}/{dataset}"):
        log_to_gui(
            LOGGER,
            "Data collection folder already exsists, please choose unique name",
            level="ERROR",
        )
        return False
    return True
