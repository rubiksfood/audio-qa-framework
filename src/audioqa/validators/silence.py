import numpy as np

from audioqa.models import AudioData, CheckResult, Severity, Status


def _count_leading_silent_frames(samples: np.ndarray, threshold: float) -> int:
    frame_amplitudes = np.max(np.abs(samples), axis=1) if samples.ndim == 2 else np.abs(samples)
    silent = frame_amplitudes < threshold

    count = 0
    for is_silent in silent:
        if not is_silent:
            break
        count += 1

    return count


def _count_trailing_silent_frames(samples: np.ndarray, threshold: float) -> int:
    frame_amplitudes = np.max(np.abs(samples), axis=1) if samples.ndim == 2 else np.abs(samples)
    silent = frame_amplitudes < threshold

    count = 0
    for is_silent in reversed(silent):
        if not is_silent:
            break
        count += 1

    return count


def validate_start_silence(
    audio: AudioData,
    max_seconds: float = 2.0,
    threshold: float = 0.001,
) -> CheckResult:
    silent_frames = _count_leading_silent_frames(audio.samples, threshold)
    silence_seconds = silent_frames / audio.sample_rate

    if silence_seconds <= max_seconds:
        return CheckResult(
            check_name="start_silence",
            status=Status.PASS,
            message=f"Start silence is {silence_seconds:.2f}s.",
            measured_value=round(silence_seconds, 2),
            expected_value=f"<= {max_seconds}s",
        )

    return CheckResult(
        check_name="start_silence",
        status=Status.WARNING,
        severity=Severity.MINOR,
        message=f"Start silence is {silence_seconds:.2f}s, exceeding limit.",
        measured_value=round(silence_seconds, 2),
        expected_value=f"<= {max_seconds}s",
    )


def validate_end_silence(
    audio: AudioData,
    max_seconds: float = 2.0,
    threshold: float = 0.001,
) -> CheckResult:
    silent_frames = _count_trailing_silent_frames(audio.samples, threshold)
    silence_seconds = silent_frames / audio.sample_rate

    if silence_seconds <= max_seconds:
        return CheckResult(
            check_name="end_silence",
            status=Status.PASS,
            message=f"End silence is {silence_seconds:.2f}s.",
            measured_value=round(silence_seconds, 2),
            expected_value=f"<= {max_seconds}s",
        )

    return CheckResult(
        check_name="end_silence",
        status=Status.WARNING,
        severity=Severity.MINOR,
        message=f"End silence is {silence_seconds:.2f}s, exceeding limit.",
        measured_value=round(silence_seconds, 2),
        expected_value=f"<= {max_seconds}s",
    )