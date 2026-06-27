import numpy as np

from audioqa.models import AudioData, CheckResult, Severity, Status


def _amplitude_to_dbfs(amplitude: float) -> float:
    if amplitude <= 0:
        return float("-inf")

    return 20 * np.log10(amplitude)


def validate_peak_level(
    audio: AudioData,
    max_peak_dbfs: float = -1.0,
) -> CheckResult:
    peak_amplitude = float(np.max(np.abs(audio.samples)))
    peak_dbfs = _amplitude_to_dbfs(peak_amplitude)

    if peak_dbfs <= max_peak_dbfs:
        return CheckResult(
            check_name="peak_level",
            status=Status.PASS,
            message=f"Peak level is {peak_dbfs:.2f} dBFS.",
            measured_value=round(peak_dbfs, 2),
            expected_value=f"<= {max_peak_dbfs} dBFS",
        )

    return CheckResult(
        check_name="peak_level",
        status=Status.WARNING,
        severity=Severity.MAJOR,
        message=f"Peak level {peak_dbfs:.2f} dBFS exceeds limit.",
        measured_value=round(peak_dbfs, 2),
        expected_value=f"<= {max_peak_dbfs} dBFS",
    )


def calculate_rms_dbfs(audio: AudioData) -> float:
    rms = float(np.sqrt(np.mean(np.square(audio.samples))))

    return _amplitude_to_dbfs(rms)


def validate_rms_range(
    audio: AudioData,
    min_rms_dbfs: float,
    max_rms_dbfs: float,
) -> CheckResult:
    rms_dbfs = calculate_rms_dbfs(audio)

    if min_rms_dbfs <= rms_dbfs <= max_rms_dbfs:
        return CheckResult(
            check_name="rms_level",
            status=Status.PASS,
            message=f"RMS level is {rms_dbfs:.2f} dBFS.",
            measured_value=round(rms_dbfs, 2),
            expected_value=f"{min_rms_dbfs} to {max_rms_dbfs} dBFS",
        )

    return CheckResult(
        check_name="rms_level",
        status=Status.WARNING,
        severity=Severity.MINOR,
        message=f"RMS level {rms_dbfs:.2f} dBFS is outside expected range.",
        measured_value=round(rms_dbfs, 2),
        expected_value=f"{min_rms_dbfs} to {max_rms_dbfs} dBFS",
    )