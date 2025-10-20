import re

from PyQt6 import QtCore, QtWidgets


class WellsSelectionPanel(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_selection()
        self.selection_layout = self.create_layout()

    def init_selection(self):
        self.selection_checkbox = QtWidgets.QCheckBox()
        self.selection_checkbox.setChecked(False)
        self.wells_selection = QtWidgets.QLineEdit()
        self.use_csv_btn = QtWidgets.QPushButton("Use CSV")
        self.use_csv_btn.clicked.connect(self._select_csv)

    def create_layout(self):
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.selection_checkbox)
        layout.addLayout(self._setup_selection_textbox())
        layout.addWidget(self.use_csv_btn)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom)
        return layout

    def _setup_selection_textbox(self):
        layout = QtWidgets.QVBoxLayout()
        label = QtWidgets.QLabel("Wells selection")
        self.wells_selection.setText("")
        layout.addWidget(label)
        layout.addWidget(self.wells_selection)
        return layout

    def _select_csv(self):
        self.csv_file = QtWidgets.QFileDialog.getOpenFileName(
            None, directory="/home", filter="Data File (*.csv)"
        )
        # self.wells_selection.setText()

    def get_selected_wells_list(self) -> list[int]:
        _wells = self.wells_selection.text()
        mapped_wells = map(int, re.findall(r"\d+", _wells))
        return list(mapped_wells)
