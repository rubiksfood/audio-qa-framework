from pathlib import Path

from audioqa.loader import load_audio
from audioqa.models import Status
from audioqa.validators.silence import validate_end_silence, validate_start_silence


def test_clean_file_has_acceptable_start_silence() -> None:
    audio = load_audio(Path("sample-audio/clean/clean_sine.wav"))

    result = validate_start_silence(audio)

    assert result.status == Status.PASS


def test_long_start_silence_warns() -> None:
    audio = load_audio(Path("sample-audio/defects/long_start_silence.wav"))

    result = validate_start_silence(audio)

    assert result.status == Status.WARNING


def test_long_end_silence_warns() -> None:
    audio = load_audio(Path("sample-audio/defects/long_end_silence.wav"))

    result = validate_end_silence(audio)

    assert result.status == Status.WARNING