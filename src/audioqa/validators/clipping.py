import numpy as np

from audioqa.models import AudioData, CheckResult, Severity, Status


def validate_clipping(
    audio: AudioData,
    clipping_threshold: float = 1.0 - (1.0 / 32768),
) -> CheckResult:
    clipped_samples = int(np.sum(np.abs(audio.samples) >= clipping_threshold))

    if clipped_samples == 0:
        return CheckResult(
            check_name="clipping",
            status=Status.PASS,
            message="No clipping detected.",
            measured_value=0,
            expected_value=f"< {clipping_threshold}",
        )

    return CheckResult(
        check_name="clipping",
        status=Status.FAIL,
        severity=Severity.CRITICAL,
        message=f"{clipped_samples} clipped samples detected.",
        measured_value=clipped_samples,
        expected_value=0,
    )