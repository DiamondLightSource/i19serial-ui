import re
from pathlib import Path

from PyQt6 import QtCore, QtWidgets

from i19serial_ui.log import LOGGER


class WellsSelectionPanel(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.logger = LOGGER
        self.init_selection()
        self.selection_layout = self.create_layout()

    def init_selection(self):
        self.selection_checkbox = QtWidgets.QCheckBox()
        self.selection_checkbox.setChecked(False)
        self.wells_selection = QtWidgets.QLineEdit()
        self.use_csv_btn = QtWidgets.QPushButton("Use CSV")
        self.use_csv_btn.clicked.connect(self._select_csv)

    def create_layout(self):
        self.wells_selection.setText("")
        wells_label = QtWidgets.QLabel("Wells selection")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(wells_label)
        layout.addWidget(self.selection_checkbox)
        layout.addWidget(self.wells_selection)
        layout.addWidget(self.use_csv_btn)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom)
        return layout

    def _select_csv(self):
        self.csv_file = QtWidgets.QFileDialog.getOpenFileName(
            None, directory="/home", filter="Data File (*.csv)"
        )[0]
        if self.csv_file:
            self.logger.info(f"Selected csv file: {self.csv_file}")
            self.wells_selection.setText(self.csv_file)

    def get_selected_wells_list(self) -> list[int]:
        if not self.selection_checkbox.isChecked():
            raise ValueError("Selection checkbox not selected")
        _wells = self.wells_selection.text()
        mapped_wells = list(map(int, re.findall(r"\d+", _wells)))
        self.logger.info(f"Selected wells: {mapped_wells}")
        return mapped_wells

    def get_csv_file_path(self) -> Path | None:
        if not self.csv_file:
            self.logger.warning("No file selected!")
            return
        return Path(self.csv_file)
