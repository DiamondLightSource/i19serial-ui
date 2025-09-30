from PyQt6 import QtCore, QtWidgets


class InputPanel(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_text_boxes()
        self.inputs_layout = self.create_input_layout()

    def init_text_boxes(self):
        self.num_images = QtWidgets.QLineEdit()
        self.time_image = QtWidgets.QLineEdit()

    def create_input_layout(self):
        layout = QtWidgets.QHBoxLayout()
        layout.addLayout(
            self._create_textbox_with_label(self.num_images, "num images", 1)
        )
        layout.addLayout(
            self._create_textbox_with_label(self.time_image, "time/image (s)", 0.2)
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
