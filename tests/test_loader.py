from pathlib import Path

from audioqa.loader import load_audio


def test_load_audio_reads_valid_wav() -> None:
    audio = load_audio(Path("sample-audio/clean/clean_sine.wav"))

    assert audio.sample_rate == 44_100
    assert audio.channels == 2
    assert audio.frames > 0
    assert audio.duration_seconds > 0
    assert audio.samples is not None