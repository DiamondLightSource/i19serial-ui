from PyQt6 import QtCore, QtWidgets


class InputPanel(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_text_boxes()
        self.inputs_layout = self.create_input_layout()

    def init_text_boxes(self):
        self.num_images = QtWidgets.QLineEdit()
        self.time_image = QtWidgets.QLineEdit()
        self.image_width = QtWidgets.QLineEdit()
        self.det_dist = QtWidgets.QLineEdit()
        self.transmission = QtWidgets.QLineEdit()
        self.well_start = QtWidgets.QLineEdit()
        self.well_end = QtWidgets.QLineEdit()
        self.series_length = QtWidgets.QLineEdit()
        self.two_theta = QtWidgets.QLineEdit()

        self.various_text_boxes = [
            (self.num_images, "No. of images", 50),
            (self.time_image, "Time images (sec)", 0.2),
            (self.image_width, "Image width (degrees)", 0.2),
            (self.det_dist, "Detector distance (mm)", 117.53),
            (self.transmission, "Transmission (%)", 5),
            (self.well_start, "Well start", 1),
            (self.well_end, "Well end", 10),
            (self.series_length, "Series length", 1),
            (self.two_theta, "2 theta (degrees)", 0),
        ]

    def create_input_layout(self):
        layout = QtWidgets.QGridLayout()
        for i, (text_box, label, default_value) in enumerate(self.various_text_boxes):
            row = i % 2
            col = i // 2
            layout.addLayout(
                self._create_textbox_with_label(text_box, label, default_value),
                row,
                col,
            )
        return layout

    def _create_textbox_with_label(
        self,
        text_box: QtWidgets.QLineEdit,
        label: str,
        default_value: float = 0,
        size: tuple = (10, 10),
    ):
        text_layout = QtWidgets.QVBoxLayout()
        text_label = QtWidgets.QLabel(label)
        text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        text_box.setText(str(default_value))
        text_box.resize(*size)
        text_box.setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom)
        text_layout.addWidget(text_label)
        text_layout.addWidget(text_box)
        return text_layout
