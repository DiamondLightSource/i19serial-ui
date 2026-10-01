from PyQt6 import QtCore, QtGui, QtWidgets

from i19serial_ui.gui.ui_utils import HutchInUse, image_file_path


class ParametricVariablesUI(QtWidgets.QWidget):
    """A new window to queue up temperature/laser/delays/etc..."""

    def __init__(
        self, hutch_in_use: HutchInUse, parent: QtWidgets.QWidget | None = None
    ) -> None:
        super().__init__(parent)
        self._hutch = hutch_in_use
        self.params_layout = self.create_layout()

    def _create_label_with_pic(
        self, name: str, pic: str
    ) -> tuple[QtWidgets.QLabel, QtWidgets.QLabel]:
        pixmap = QtGui.QPixmap(image_file_path(pic))
        pixmap.scaledToWidth(30)
        pixmap.scaledToHeight(30)
        lbl_pic = QtWidgets.QLabel()
        lbl_pic.setFixedSize(30, 30)
        lbl_pic.setPixmap(pixmap)
        lbl_pic.setScaledContents(True)
        lbl = QtWidgets.QLabel(name)
        lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        return lbl, lbl_pic

    def _create_sleep_box(self):
        self.sleep_group = QtWidgets.QGroupBox()
        sleep_layout = QtWidgets.QHBoxLayout()
        self.sleep_box = QtWidgets.QLineEdit()
        self.sleep_box.setFixedWidth(50)
        self.queue_sleep = QtWidgets.QPushButton("Queue")
        self.queue_sleep.setFixedWidth(50)
        _sleep_lbl, _sleep_pic = self._create_label_with_pic("Sleep (s)", "sleep.png")
        sleep_layout.addWidget(_sleep_pic)
        sleep_layout.addWidget(_sleep_lbl)
        sleep_layout.addWidget(self.sleep_box)
        sleep_layout.addWidget(self.queue_sleep)
        self.sleep_group.setLayout(sleep_layout)

    def _create_light_box(self):
        self.light_group = QtWidgets.QGroupBox()
        light_layout = QtWidgets.QHBoxLayout()
        self.light_box = QtWidgets.QLineEdit()
        self.light_box.setFixedWidth(50)
        self.queue_light = QtWidgets.QPushButton("Queue")
        self.queue_light.setFixedWidth(50)
        _light_lbl, _light_pic = self._create_label_with_pic("Light (s)", "laser.png")
        light_layout.addWidget(_light_pic)
        light_layout.addWidget(_light_lbl)
        light_layout.addWidget(self.light_box)
        light_layout.addWidget(self.queue_light)
        self.light_group.setLayout(light_layout)

    def _create_temp_box(self):
        self.temp_group = QtWidgets.QGroupBox()
        temp_layout = QtWidgets.QHBoxLayout()
        self.temp_box = QtWidgets.QLineEdit()
        self.temp_box.setFixedWidth(50)
        self.queue_temp = QtWidgets.QPushButton("Queue")
        self.queue_temp.setFixedWidth(50)
        _temp_lbl, _temp_pic = self._create_label_with_pic("Temp (K)", "temp.png")
        temp_layout.addWidget(_temp_pic)
        temp_layout.addWidget(_temp_lbl)
        temp_layout.addWidget(self.temp_box)
        temp_layout.addWidget(self.queue_temp)
        self.temp_group.setLayout(temp_layout)

    def _create_pressure_box(
        self,
        label: str,
        group: QtWidgets.QGroupBox,
        text_box: QtWidgets.QLineEdit,
        btn: QtWidgets.QPushButton,
    ):
        pres_layout = QtWidgets.QHBoxLayout()
        _pres_lbl, _pres_pic = self._create_label_with_pic(
            f"Pres. {label}", "pressure.png"
        )
        text_box.setFixedWidth(50)
        btn.setFixedWidth(50)
        btn.setEnabled(False)
        pres_layout.addWidget(_pres_pic)
        pres_layout.addWidget(_pres_lbl)
        pres_layout.addWidget(text_box)
        pres_layout.addWidget(btn)
        group.setLayout(pres_layout)

    def _setup_common_variables(self):
        self._create_sleep_box()
        self._create_light_box()
        self._create_temp_box()

    def _setup_eh2_specific_variables(self):
        self.pres_1_group = QtWidgets.QGroupBox()
        self.pres_1_box = QtWidgets.QLineEdit()
        self.queue_pres_1 = QtWidgets.QPushButton("Queue")
        self._create_pressure_box(
            "MFC1", self.pres_1_group, self.pres_1_box, self.queue_pres_1
        )
        self.pres_2_group = QtWidgets.QGroupBox()
        self.pres_2_box = QtWidgets.QLineEdit()
        self.queue_pres_2 = QtWidgets.QPushButton("Queue")
        self._create_pressure_box(
            "MFC2", self.pres_2_group, self.pres_2_box, self.queue_pres_2
        )

    def create_layout(self):
        layout = QtWidgets.QGridLayout()
        self._setup_common_variables()
        layout.addWidget(self.sleep_group, 0, 0)
        layout.addWidget(self.light_group, 0, 1)
        layout.addWidget(self.temp_group, 0, 2)
        if self._hutch == HutchInUse.EH2:
            self._setup_eh2_specific_variables()
            layout.addWidget(self.pres_1_group, 1, 0)
            layout.addWidget(self.pres_2_group, 1, 1)
        return layout
