# NOTE For actual logs, we'll use the dodal/blueapi logger
# But we do need something that prints to the UI
import logging
from pathlib import Path

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
    if level != logging.DEBUG:
        logger.log(getattr(logging, level.upper()), f"{output_str}")


def setup_logging():
    logdir = Path("/tmp/serial-logs")  # TODO add actual choice depending on visit
    logdir.mkdir(parents=True, exist_ok=True)

    logfile = logdir / "i19serial-ui.log"

    file_formatter = logging.Formatter(
        "%(asctime)s %(levelname)s || %(name)s %(message)s", datefmt="%Y-%m-%d %I:%M:%S"
    )
    FH = logging.FileHandler(logfile, mode="a", encoding="utf-8")  # noqa: N806
    FH.setLevel(logging.DEBUG)
    FH.setFormatter(file_formatter)
    LOGGER.addHandler(FH)


def tidy_up_logging(loggers: list[logging.Logger]):
    for logger in loggers:
        for handler in logger.handlers:
            handler.close()
        logger.handlers.clear()
