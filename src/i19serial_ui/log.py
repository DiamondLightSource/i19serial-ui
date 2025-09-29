# NOTE For actual logs, we'll use the dodal/blueapi logger
# But we do need something that prints to the UI
import logging

from PyQt6.QtCore import QObject, pyqtSignal

LOGGER = logging.getLogger("i19serial-ui")
LOGGER.setLevel(logging.DEBUG)


class GuiWindowLogHandler(logging.Handler, QObject):
    signalLog: pyqtSignal = pyqtSignal(str)  # noqa: N815
    flushOnClose: bool = True  # noqa: N815

    def __init__(self):
        super().__init__()
        QObject.__init__(self)
        gui_formatter = logging.Formatter("%(message)s")

        self.setFormatter(gui_formatter)
        self.setLevel(logging.INFO)

    def emit(self, record: logging.LogRecord):
        msg = self.format(record)
        self.signalLog.emit(msg)

    def flush(self):
        pass


def log_to_gui(logger: logging.Logger, output_str: str, level: str = "INFO"):
    logger.log(getattr(logging, level.upper()), f"{output_str}")


def tidy_up_logging(loggers: list[logging.Logger]):
    for logger in loggers:
        for handler in logger.handlers:
            handler.close()
        logger.handlers.clear()
