from pathlib import Path

from audioqa.loader import load_audio
from audioqa.models import Status
from audioqa.validators.clipping import validate_clipping


def test_clean_file_has_no_clipping() -> None:
    audio = load_audio(Path("sample-audio/clean/clean_sine.wav"))

    result = validate_clipping(audio)

    assert result.status == Status.PASS


def test_clipped_file_fails_clipping_check() -> None:
    audio = load_audio(Path("sample-audio/defects/clipped_sine.wav"))

    result = validate_clipping(audio)

    assert result.status == Status.FAIL