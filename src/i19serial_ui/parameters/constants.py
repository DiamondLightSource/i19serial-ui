from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class SampleStageDeviceName:
    NEWPORT = "diffractometer"
    BEAMSTOP = "beamstop"
