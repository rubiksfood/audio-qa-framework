from pathlib import Path

from audioqa.loader import load_audio
from audioqa.models import Status
from audioqa.validators.metadata import validate_channels, validate_sample_rate


def test_sample_rate_passes_when_allowed() -> None:
    audio = load_audio(Path("sample-audio/clean/clean_sine.wav"))

    result = validate_sample_rate(audio, {44_100})

    assert result.status == Status.PASS


def test_sample_rate_fails_when_not_allowed() -> None:
    audio = load_audio(Path("sample-audio/clean/clean_sine.wav"))

    result = validate_sample_rate(audio, {48_000})

    assert result.status == Status.FAIL


def test_channels_pass_when_allowed() -> None:
    audio = load_audio(Path("sample-audio/clean/clean_sine.wav"))

    result = validate_channels(audio, {2})

    assert result.status == Status.PASS