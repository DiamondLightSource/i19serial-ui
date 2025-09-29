import logging
from unittest.mock import MagicMock, patch

from i19serial_ui.log import (
    GuiWindowLogHandler,
    _get_logging_path,
    log_to_gui,
    tidy_up_logging,
)


def test_gui_log_handler():
    gui_handler = GuiWindowLogHandler()
    gui_handler.signalLog = MagicMock()
    msg = "Hello"
    gui_handler.emit(logging.LogRecord("Info", logging.INFO, "", 0, msg, None, None))

    gui_handler.signalLog.emit.assert_called_once_with(msg)


def test_tidy_up_logging():
    test_logger = logging.getLogger("test")
    test_logger.addHandler(logging.StreamHandler())

    assert len(test_logger.handlers) == 1
    tidy_up_logging([test_logger])
    assert len(test_logger.handlers) == 0


def test_log_to_gui():
    mock_logger = MagicMock()

    log_to_gui(mock_logger, "hello, test")

    mock_logger.log.assert_called_once()


@patch("i19serial_ui.log.Path.mkdir")
@patch("i19serial_ui.log.environ")
def test_get_logging_path_if_on_beamline(
    mock_environ: MagicMock, mock_mkdir: MagicMock
):
    mock_environ.get.return_value = "i19-1"
    log_path = _get_logging_path()
    assert log_path.as_posix() == "/tmp"
    mock_mkdir.assert_called_once()


@patch("i19serial_ui.log.Path.mkdir")
@patch("i19serial_ui.log.environ")
def test_logging_path_if_not_on_beamline(
    mock_environ: MagicMock, mock_mkdir: MagicMock
):
    mock_environ.get.return_value = None
    log_path = _get_logging_path()
    assert log_path.as_posix() == "tmp/serial-logs"
    mock_mkdir.assert_called_once()
