from enum import StrEnum

from pydantic.dataclasses import dataclass


class GridType(StrEnum):
    POLYMER = "polymer"
    SILICON = "silicon"
    KAPTON400 = "kapton"
    FILM = "film"


@dataclass
class Grid:
    """Description of the 2D grid."""

    size_x: int
    size_z: int

    grid_type: GridType = GridType.POLYMER

    @property
    def dim_xz_steps(self) -> tuple[float, float]:
        match self.grid_type:
            case GridType.POLYMER:
                return (0.120, 0.120)
            case GridType.SILICON:
                return (0.125, 0.125)
            case GridType.KAPTON400:
                return (0.120, 0.120)
            case GridType.FILM:
                return (0.100, 0.100)

    @property
    def city_block_x(self) -> float:
        return (self.size_x - 1) * self.dim_xz_steps[0]

    @property
    def city_block_z(self) -> float:
        return (self.size_z - 1) * self.dim_xz_steps[1]

    def get_grid_positions(self) -> dict[str, float]:
        "Returns index of TL, TR, BL, BR positions in coords list."
        tl_pos = 0.0
        tr_pos = self.size_x - 1
        if (self.size_z % 2) == 0:
            bl_pos = self.size_x * self.size_z - 1
            br_pos = self.size_x * (self.size_z - 1) - 1
        else:
            bl_pos = self.size_x * (self.size_z - 1) - 1
            br_pos = self.size_x * self.size_z - 1
        pos_dict = {"posTL": tl_pos, "posTR": tr_pos, "posBL": bl_pos, "posBR": br_pos}
        return pos_dict
