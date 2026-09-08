from PyQt6 import QtWidgets

from i19serial_ui.gui.ui_utils import HutchInUse


class ParametricVariablesUI(QtWidgets.QWidget):
    """A new window to queue up temperature/laser/delays/etc..."""

    def __init__(self, hutch_in_use: HutchInUse) -> None:
        super().__init__()
        self._hutch = hutch_in_use
        self._setup_layout()

    def _create_text_boxes(self):
        self._sleep_box = QtWidgets.QLineEdit()
        self._light_box = QtWidgets.QLineEdit()
        self._temp_box = QtWidgets.QLineEdit()
        self.text_boxes = [self._sleep_box, self._light_box, self._temp_box]
        if self._hutch == HutchInUse.EH2:
            self._pres1_box = QtWidgets.QLineEdit()
            self._pres2_box = QtWidgets.QLineEdit()
            self.text_boxes.append(self._pres1_box)
            self.text_boxes.append(self._pres2_box)

    def _setup_eh1_variables(self):
        pass

    def _setup_eh2_variables(self):
        self._create_text_boxes()

    # Probably a slightly better way?
    def _setup_layout(self):
        match self._hutch:
            case HutchInUse.EH1:
                self._setup_eh1_variables()
            case HutchInUse.EH2:
                self._setup_eh2_variables()
        # self._create_text_boxes()
