import pytest

from i19serial_ui.parameters.queue import ElementType, QueueElement


@pytest.mark.parametrize(
    "plan_name, params, kind, expected_label",
    [
        ("collection_plan", {"dataset": "test"}, "collection", "Run collection test"),
        ("temperature_plan", {"temperature": 10}, "variable", "Run temperature_plan"),
    ],
)
def test_queue_element(plan_name: str, params: dict, kind: str, expected_label: str):
    element = QueueElement(plan_name=plan_name, plan_params=params, element_type=kind)  # type: ignore

    assert element.id
    assert element.element_type == ElementType(kind)
    assert element.element_label == expected_label
