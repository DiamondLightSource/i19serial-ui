from typing import Any

from pydantic import Field
from pydantic.dataclasses import dataclass


@dataclass
class QueueElement:
    plan_name: str
    plan_params: dict[str, Any]

    index: int = Field(default=0)

    @property
    def element_label(self):
        return f"Run {self.plan_params['dataset']}"
        # return f"Run {self.plan_name}"

    def update_index(self, i: int):
        self.index = i
