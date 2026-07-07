from enum import StrEnum
from typing import Any
from uuid import uuid4

from pydantic import Field
from pydantic.dataclasses import dataclass


class ElementType(StrEnum):
    COLLECTION = "collection"
    VARIABLE = "variable"


# I could also use uuid to give them an unique id and make things easier?


@dataclass
class QueueElement:
    plan_name: str
    plan_params: dict[str, Any]

    element_type: ElementType = Field(default=ElementType.COLLECTION)
    id: str = Field(default_factory=lambda: uuid4().hex)

    @property
    def element_label(self) -> str:
        if self.element_type == ElementType.COLLECTION:
            return f"Run collection {self.plan_params['dataset']}"
        else:
            return f"Run {self.plan_name}"
