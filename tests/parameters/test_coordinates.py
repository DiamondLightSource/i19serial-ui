from unittest.mock import mock_open, patch

from i19serial_ui.parameters.coordinates import Coord3D, Coordinates

FAKE_CS_JSON = {
    "top_left": (0.1, 0.0, 1.2),
    "top_right": (0.1, 0.0, 1.4),
    "bottom_left": (0.3, 0.0, 1.2),
}


def test_upload_coordinates_from_json():
    with (
        patch("i19serial_ui.parameters.coordinates.open", mock_open()),
        patch("i19serial_ui.parameters.coordinates.json.load") as mock_cs_json,
    ):
        mock_cs_json.return_value = FAKE_CS_JSON
        new_coords = Coordinates.from_json(mock_cs_json)

        assert new_coords.top_left == Coord3D(*FAKE_CS_JSON["top_left"])
        assert new_coords.top_right == Coord3D(*FAKE_CS_JSON["top_right"])
        assert new_coords.bottom_left == Coord3D(*FAKE_CS_JSON["bottom_left"])
