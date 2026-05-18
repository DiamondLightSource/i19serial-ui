from typing import Any

from pydantic.dataclasses import dataclass


@dataclass
class QueueElement:
    num: int
    plan_name: str
    plan_params: dict[str, Any]

    @property
    def element_label(self):
        return f"run_{self.plan_name}_pos_{self.num}"
