from enum import StrEnum
from typing import Any
from uuid import uuid4

from pydantic import Field
from pydantic.dataclasses import dataclass

DO_NOT_DISPLAY = [
    "aperture_request",
    "visit",
    "dataset",
    "wells_to_collect",
    "detector_type",
]


class ElementType(StrEnum):
    COLLECTION = "collection"
    SLEEP = "sleep"
    LASER = "laser"
    TEMPERATURE = "temperature"
    PRESSURE = "pressure"


@dataclass
class QueueElement:
    plan_name: str
    plan_params: dict[str, Any]

    element_type: ElementType = Field(default=ElementType.COLLECTION)
    id: str = Field(default_factory=lambda: uuid4().hex)

    @property
    def element_label(self) -> str:
        if self.element_type == ElementType.COLLECTION:
            return f"Run collection {self.plan_params['parameters']['dataset']}"
        else:
            return f"Run {self.plan_name}"

    def display_params(self) -> dict[str, Any]:
        if self.element_type != ElementType.COLLECTION:
            return self.plan_params
        else:
            params = {
                k: v
                for k, v in self.plan_params["parameters"].items()
                if k not in DO_NOT_DISPLAY
            }
            params["tot_num_wells"] = len(
                self.plan_params["parameters"]["wells_to_collect"]
            )
            return params
