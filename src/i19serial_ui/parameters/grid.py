from enum import StrEnum

from pydantic.dataclasses import dataclass

from i19serial_ui.parameters.coordinates import FiducialPosition


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
        pos_dict = {
            "top_left": tl_pos,
            "top_right": tr_pos,
            "bottom_left": bl_pos,
            "bottom_right": br_pos,
        }
        return pos_dict

    def get_fiducial_translation(
        self, fiducial: FiducialPosition, known_fiducial: FiducialPosition
    ) -> tuple[float, float, float]:
        v = (0, 0, 0)
        match fiducial:
            case FiducialPosition.TL:
                if known_fiducial == FiducialPosition.TR:
                    v = (-self.city_block_x, 0, 0)
                if known_fiducial == FiducialPosition.BL:
                    v = (0, 0, self.city_block_z)
            case FiducialPosition.TR:
                if known_fiducial == FiducialPosition.TL:
                    v = (self.city_block_x, 0, 0)
                if known_fiducial == FiducialPosition.BL:
                    v = (self.city_block_x, 0, -self.city_block_z)
            case FiducialPosition.BL:
                if known_fiducial == FiducialPosition.TL:
                    v = (0, 0, -self.city_block_z)
                if known_fiducial == FiducialPosition.BL:
                    v = (-self.city_block_x, 0, -self.city_block_z)
        return v
