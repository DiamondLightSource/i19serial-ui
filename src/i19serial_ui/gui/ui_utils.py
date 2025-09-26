from importlib.resources import files

from i19serial_ui import assets

IMAGES_PATH = files(assets)


def image_file_path(filename: str) -> str:
    full_path = IMAGES_PATH.joinpath(filename)
    return full_path.as_posix()  # type: ignore
