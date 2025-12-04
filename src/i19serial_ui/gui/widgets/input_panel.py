from PyQt6 import QtWidgets


class InputPanel(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self.init_text_boxes()
        self.inputs_layout = self.create_input_layout()

    def init_text_boxes(self):
        self.visit_path = QtWidgets.QLineEdit()
        self.dataset = QtWidgets.QLineEdit()
        self.prefix = QtWidgets.QLineEdit()
        self.num_images = QtWidgets.QLineEdit()
        self.time_image = QtWidgets.QLineEdit()
        self.image_width = QtWidgets.QLineEdit()
        self.det_dist = QtWidgets.QLineEdit()
        self.transmission = QtWidgets.QLineEdit()
        self.well_start = QtWidgets.QLineEdit()
        self.well_end = QtWidgets.QLineEdit()
        self.series_length = QtWidgets.QLineEdit()
        self.two_theta = QtWidgets.QLineEdit()
        self.rotation_start = QtWidgets.QLineEdit()

    def create_input_layout(self):
        main_layout = QtWidgets.QVBoxLayout()
        self.visit_path.setReadOnly(True)
        visit_layout = self._create_textbox_with_label(self.visit_path, "Visit", "")
        dataset_layout = self._create_dataset_layout()
        params_layout = self._create_params_layout()
        main_layout.addLayout(visit_layout)
        main_layout.addLayout(dataset_layout)
        main_layout.addLayout(params_layout)
        return main_layout

    def _create_dataset_layout(self):
        layout = QtWidgets.QHBoxLayout()
        layout.addLayout(self._create_textbox_with_label(self.dataset, "Dataset", ""))
        layout.addLayout(self._create_textbox_with_label(self.prefix, "Prefix", ""))
        return layout

    def _create_params_layout(self):
        layout = QtWidgets.QGridLayout()
        layout.addLayout(
            self._create_textbox_with_label(self.num_images, "No. images", 50), 0, 0
        )
        layout.addLayout(
            self._create_textbox_with_label(self.time_image, "Time image (s)", 0.2),
            0,
            1,
        )
        layout.addLayout(
            self._create_textbox_with_label(self.image_width, "Image width (deg)", 0.2),
            0,
            2,
        )
        layout.addLayout(
            self._create_textbox_with_label(self.det_dist, "Det distance (mm)", 117.53),
            0,
            3,
        )
        layout.addLayout(
            self._create_textbox_with_label(self.two_theta, "2 theta (deg)", 0), 0, 4
        )
        layout.addLayout(
            self._create_textbox_with_label(self.rotation_start, "Phi start (deg)", 0),
            1,
            0,
        )  # For now just assumes phi rotation.
        # TODO see https://github.com/DiamondLightSource/i19serial-ui/issues/25
        layout.addLayout(
            self._create_textbox_with_label(self.well_start, "Well start", 1), 1, 1
        )
        layout.addLayout(
            self._create_textbox_with_label(self.well_end, "Well end", 10), 1, 2
        )
        layout.addLayout(
            self._create_textbox_with_label(self.series_length, "Series length", 1),
            1,
            3,
        )
        layout.addLayout(
            self._create_textbox_with_label(self.transmission, "Transmission (%)", 5),
            1,
            4,
        )
        return layout

    def _create_textbox_with_label(
        self,
        text_box: QtWidgets.QLineEdit,
        label: str,
        default_value: float | str = 0,
    ):
        text_layout = QtWidgets.QVBoxLayout()
        text_label = QtWidgets.QLabel(label)
        text_box.setText(str(default_value))
        text_layout.addWidget(text_label)
        text_layout.addWidget(text_box)
        return text_layout
