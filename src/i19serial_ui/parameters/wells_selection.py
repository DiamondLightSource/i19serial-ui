from pydantic import BaseModel, computed_field


class WellsSelection(BaseModel):
    first: int
    last: int
    selected: list[int]  # NOTE this is 1-indexed
    series_length: int  # How many in the same detector arm
    manual_selection_enabled: bool = False

    @computed_field
    @property
    def num_series(self) -> int:
        if len(self.selected) % self.series_length == 0:
            return len(self.selected) // self.series_length
        else:
            return len(self.selected) // self.series_length + 1

    @property
    def num_wells_to_collect(self) -> int:
        return len(self.selected)
