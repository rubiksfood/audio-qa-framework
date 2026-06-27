from pathlib import Path

import soundfile as sf

from audioqa.models import AudioData


def load_audio(file_path: str | Path) -> AudioData:
    """Load an audio file and return its metadata and sample data."""

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    samples, sample_rate = sf.read(
        path,
        dtype="float32",
        always_2d=False,
    )

    info = sf.info(path)

    return AudioData(
        path=path,
        samples=samples,
        sample_rate=sample_rate,
        channels=info.channels,
        frames=info.frames,
        duration_seconds=info.frames / info.samplerate,
        format=info.format,
        subtype=info.subtype,
    )