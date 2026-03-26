import json
from enum import StrEnum
from pathlib import Path
from typing import NamedTuple

from pydantic import BaseModel

COORD_FILE_PATH = Path("/dls_sw/i19-2/scripts/")  # Temporary


class Coord3D(NamedTuple):
    """3D coordinates of the chip"""

    x: float
    y: float
    z: float


class Coordinates(BaseModel):
    top_left: Coord3D
    top_right: Coord3D
    bottom_left: Coord3D

    @classmethod
    def from_json(cls, filename: Path | str):
        with open(filename) as fh:
            raw_params = json.load(fh)
        return cls(**raw_params)


class FiducialPosition(StrEnum):
    TL = "top left"
    TR = "top right"
    BL = "bottom left"
