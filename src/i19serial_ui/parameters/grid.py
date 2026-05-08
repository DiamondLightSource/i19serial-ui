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

    x_steps: int
    z_steps: int

    grid_type: GridType = GridType.POLYMER

    @property
    def x_step_size(self) -> float:
        return self.get_dim_xz_steps()[0]

    @property
    def z_step_size(self) -> float:
        return self.get_dim_xz_steps()[1]

    @property
    def city_block_x(self) -> float:
        return (self.x_steps - 1) * self.x_step_size

    @property
    def city_block_z(self) -> float:
        return (self.z_steps - 1) * self.z_step_size

    @property
    def total_num_wells(self) -> int:
        return self.x_steps * self.z_steps

    def get_dim_xz_steps(self) -> tuple[float, float]:
        match self.grid_type:
            case GridType.POLYMER:
                return (0.120, 0.120)
            case GridType.SILICON:
                return (0.125, 0.125)
            case GridType.KAPTON400:
                return (0.120, 0.120)
            case GridType.FILM:
                return (0.100, 0.100)

    def get_grid_positions(self) -> dict[FiducialPosition, int]:
        "Returns index of TL, TR, BL positions in coords list."
        tl_pos = 0
        tr_pos = self.x_steps - 1
        if (self.z_steps % 2) == 0:
            bl_pos = self.x_steps * self.z_steps - 1
        else:
            bl_pos = self.x_steps * (self.z_steps - 1) - 1
        pos_dict = {
            FiducialPosition.TL: tl_pos,
            FiducialPosition.TR: tr_pos,
            FiducialPosition.BL: bl_pos,
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
                if known_fiducial == FiducialPosition.TR:
                    v = (-self.city_block_x, 0, -self.city_block_z)
        return v
