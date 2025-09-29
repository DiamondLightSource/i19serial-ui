"""
Small molecule x-ray diffraction UI for fixed target serial collections on beamline I19.
"""

import argparse
from collections.abc import Sequence
from enum import IntEnum

from i19serial_ui.gui.serial_gui_eh2 import start_eh2_ui

from . import __version__

__all__ = ["main"]


class HutchChoice(IntEnum):
    EH1 = 1
    EH2 = 2


def main(args_in: Sequence[str] | None = None) -> None:
    """Argument parser for the CLI."""
    version_parser = argparse.ArgumentParser(add_help=False)
    version_parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"I19 serial UI v{__version__}",
    )

    parser = argparse.ArgumentParser(description=__doc__, parents=[version_parser])
    parser.add_argument(
        "hutch",
        type=int,
        choices=list(HutchChoice),
        help="Hutch in use for the current beamtime.",
    )
    args = parser.parse_args(args_in)

    if args.hutch == HutchChoice.EH1:
        print("EH1 serial GUI not implemented yet")
    if args.hutch == HutchChoice.EH2:
        print("Starting UI for EH2 ...")
        start_eh2_ui()


# Interface for ``python -m i19serial_ui -v``
if __name__ == "__main__":
    main()
