from audioqa.models import AudioData, CheckResult, Severity, Status


def validate_sample_rate(audio: AudioData, allowed_sample_rates: set[int]) -> CheckResult:
    if audio.sample_rate in allowed_sample_rates:
        return CheckResult(
            check_name="sample_rate",
            status=Status.PASS,
            message=f"Sample rate is {audio.sample_rate} Hz.",
            measured_value=audio.sample_rate,
            expected_value=", ".join(map(str, sorted(allowed_sample_rates))),
        )

    return CheckResult(
        check_name="sample_rate",
        status=Status.FAIL,
        severity=Severity.MAJOR,
        message=f"Sample rate {audio.sample_rate} Hz is not allowed.",
        measured_value=audio.sample_rate,
        expected_value=", ".join(map(str, sorted(allowed_sample_rates))),
    )


def validate_channels(audio: AudioData, allowed_channels: set[int]) -> CheckResult:
    if audio.channels in allowed_channels:
        return CheckResult(
            check_name="channels",
            status=Status.PASS,
            message=f"Channel count is {audio.channels}.",
            measured_value=audio.channels,
            expected_value=", ".join(map(str, sorted(allowed_channels))),
        )

    return CheckResult(
        check_name="channels",
        status=Status.FAIL,
        severity=Severity.MAJOR,
        message=f"Channel count {audio.channels} is not allowed.",
        measured_value=audio.channels,
        expected_value=", ".join(map(str, sorted(allowed_channels))),
    )


def validate_duration(
    audio: AudioData,
    min_seconds: float | None = None,
    max_seconds: float | None = None,
) -> CheckResult:
    duration = audio.duration_seconds

    if min_seconds is not None and duration < min_seconds:
        return CheckResult(
            check_name="duration",
            status=Status.FAIL,
            severity=Severity.MAJOR,
            message=f"Duration {duration:.2f}s is shorter than minimum.",
            measured_value=round(duration, 2),
            expected_value=f">= {min_seconds}s",
        )

    if max_seconds is not None and duration > max_seconds:
        return CheckResult(
            check_name="duration",
            status=Status.FAIL,
            severity=Severity.MAJOR,
            message=f"Duration {duration:.2f}s exceeds maximum.",
            measured_value=round(duration, 2),
            expected_value=f"<= {max_seconds}s",
        )

    return CheckResult(
        check_name="duration",
        status=Status.PASS,
        message=f"Duration is {duration:.2f}s.",
        measured_value=round(duration, 2),
    )