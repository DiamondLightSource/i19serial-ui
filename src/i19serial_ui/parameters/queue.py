from typing import Any

from pydantic.dataclasses import dataclass


@dataclass
class QueueElement:
    plan_name: str
    plan_params: dict[str, Any]

    @property
    def element_label(self):
        return f"Run {self.plan_params['dataset']}"
        # return f"Run {self.plan_name}"

    # NOTE this will only work whle I have collections, as soon as I add variables
    # there will be no dataset in parameters - so need something better
