from audioqa.loader import read_metadata


def test_read_metadata_valid_file():
    metadata = read_metadata("sample-audio/clean/test.wav")

    assert metadata.sample_rate > 0
    assert metadata.channels > 0
    assert metadata.frames > 0
    assert metadata.duration_seconds > 0