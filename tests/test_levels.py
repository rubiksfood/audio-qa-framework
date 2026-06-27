from pathlib import Path

from audioqa.loader import load_audio
from audioqa.models import Status
from audioqa.validators.levels import validate_peak_level


def test_clean_file_peak_level_passes() -> None:
    audio = load_audio(Path("sample-audio/clean/clean_sine.wav"))

    result = validate_peak_level(audio, max_peak_dbfs=-1.0)

    assert result.status == Status.PASS


def test_clipped_file_peak_level_warns() -> None:
    audio = load_audio(Path("sample-audio/defects/clipped_sine.wav"))

    result = validate_peak_level(audio, max_peak_dbfs=-1.0)

    assert result.status == Status.WARNING