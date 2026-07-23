from PyQt6 import QtWidgets

from i19serial_ui.blueapi_tools.blueapi_client import SerialBlueapiClient

# Wrapper around bps.mv from dodal.plan_stubs
MOVE_PLAN = "move"


class SampleAlignment(QtWidgets.QWidget):
    def __init__(
        self,
        blueapi_client: SerialBlueapiClient,
        parent: QtWidgets.QWidget | None = None,
    ):
        super().__init__(parent)
        self.client = blueapi_client
        self.init_arrow_buttons()

    def init_arrow_buttons(self):
        pass

    def create_layout(self):
        pass
