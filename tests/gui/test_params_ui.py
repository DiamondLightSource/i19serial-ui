import pytest
from PyQt6 import QtWidgets

from i19serial_ui.gui.ui_utils import HutchInUse
from i19serial_ui.gui.widgets.queue.parametric_vars_ui import ParametricVariablesUI


@pytest.fixture
def mock_vars_widget_eh2(qtbot):
    test_vars = ParametricVariablesUI(HutchInUse.EH2)
    qtbot.addWidget(test_vars)
    return test_vars


def test_vars_widget(mock_vars_widget_eh2):
    assert isinstance(mock_vars_widget_eh2.params_layout, QtWidgets.QGridLayout)

    # EH2 has 5 widget, EH1 just 3 for now
    assert mock_vars_widget_eh2.params_layout.count() == 5
    # First item in group is a label with pic
    assert isinstance(
        mock_vars_widget_eh2.sleep_group.layout().itemAt(0).widget(),
        QtWidgets.QLabel,
    )
    # Second one is actual label
    light_lbl = mock_vars_widget_eh2.light_group.layout().itemAt(1).widget()
    assert light_lbl.text() == "Light (s)"
    # Third is a text box
    assert isinstance(
        mock_vars_widget_eh2.temp_group.layout().itemAt(2).widget(), QtWidgets.QLineEdit
    )
    # Forth is a button
    assert isinstance(
        mock_vars_widget_eh2.sleep_group.layout().itemAt(3).widget(),
        QtWidgets.QPushButton,
    )


def test_queue_pressure_buttons_are_disabled(mock_vars_widget_eh2):
    pres_1_btn = mock_vars_widget_eh2.queue_pres_1
    assert not pres_1_btn.isEnabled()

    pres_2_btn = mock_vars_widget_eh2.queue_pres_2
    assert not pres_2_btn.isEnabled()
