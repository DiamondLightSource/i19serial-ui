from typing import Any

from pydantic.dataclasses import dataclass


@dataclass
class QueueElement:
    plan_name: str
    plan_params: dict[str, Any]

    @property
    def element_label(self):
        return f"Run {self.plan_name}"
