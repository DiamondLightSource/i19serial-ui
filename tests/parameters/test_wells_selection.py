import pytest

from i19serial_ui.parameters.wells_selection import WellsSelection


@pytest.fixture
def dummy_wells_settings():
    return {
        "first": 0,
        "last": 5,
        "selected": [1, 3, 5],
        "series_length": 3,
        "manual_selection_enabled": True,
    }


def test_wells_selection(dummy_wells_settings):
    params = WellsSelection(**dummy_wells_settings)

    assert params.num_wells_to_collect == 3
    assert params.num_series == 1


def test_wells_selection_with_multiple_series(dummy_wells_settings):
    dummy_wells_settings["series_length"] = 2

    params = WellsSelection(**dummy_wells_settings)

    assert params.num_series == 2
