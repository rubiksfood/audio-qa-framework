from dataclasses import dataclass
from enum import Enum
from pathlib import Path

import numpy as np
import numpy.typing as npt


class Status(str, Enum):
    PASS = "PASS"
    WARNING = "WARNING"
    FAIL = "FAIL"


class Severity(str, Enum):
    CRITICAL = "critical"
    MAJOR = "major"
    MINOR = "minor"
    INFO = "info"


@dataclass(frozen=True)
class AudioData:
    path: Path
    samples: npt.NDArray[np.float32]
    sample_rate: int
    channels: int
    frames: int
    duration_seconds: float
    format: str
    subtype: str


@dataclass(frozen=True)
class CheckResult:
    check_name: str
    status: Status
    message: str
    severity: Severity | None = None
    measured_value: float | int | str | None = None
    expected_value: float | int | str | None = None