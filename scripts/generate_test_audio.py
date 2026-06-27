from pathlib import Path

import numpy as np
import soundfile as sf


SAMPLE_RATE = 44_100
DURATION_SECONDS = 3.0
AMPLITUDE = 0.5

OUTPUT_DIR = Path("sample-audio")


def create_time_axis(duration_seconds: float, sample_rate: int) -> np.ndarray:
    total_samples = int(duration_seconds * sample_rate)

    return np.linspace(
        0,
        duration_seconds,
        total_samples,
        endpoint=False,
        dtype=np.float32,
    )


def create_sine_wave(
    frequency_hz: float = 440.0,
    duration_seconds: float = DURATION_SECONDS,
    sample_rate: int = SAMPLE_RATE,
    amplitude: float = AMPLITUDE,
) -> np.ndarray:
    time = create_time_axis(duration_seconds, sample_rate)

    return amplitude * np.sin(2 * np.pi * frequency_hz * time)


def to_stereo(mono_audio: np.ndarray) -> np.ndarray:
    return np.column_stack((mono_audio, mono_audio))


def write_wav(path: Path, audio: np.ndarray, sample_rate: int = SAMPLE_RATE) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    sf.write(
        file=path,
        data=audio,
        samplerate=sample_rate,
        subtype="PCM_16",
    )


def create_clean_sine() -> None:
    sine = create_sine_wave()
    stereo = to_stereo(sine)

    write_wav(OUTPUT_DIR / "clean" / "clean_sine.wav", stereo)


def create_clipped_sine() -> None:
    sine = create_sine_wave(amplitude=1.2)

    clipped = np.clip(sine, -1.0, 1.0)
    stereo = to_stereo(clipped)

    write_wav(OUTPUT_DIR / "defects" / "clipped_sine.wav", stereo)


def create_silent_file() -> None:
    total_samples = int(DURATION_SECONDS * SAMPLE_RATE)

    silence = np.zeros(total_samples, dtype=np.float32)
    stereo = to_stereo(silence)

    write_wav(OUTPUT_DIR / "defects" / "silent_file.wav", stereo)


def create_long_start_silence() -> None:
    silence_duration = 2.5
    tone_duration = DURATION_SECONDS - silence_duration

    silence = np.zeros(int(silence_duration * SAMPLE_RATE), dtype=np.float32)
    tone = create_sine_wave(duration_seconds=tone_duration)

    audio = np.concatenate((silence, tone))
    stereo = to_stereo(audio)

    write_wav(OUTPUT_DIR / "defects" / "long_start_silence.wav", stereo)


def create_long_end_silence() -> None:
    tone_duration = 0.5
    silence_duration = DURATION_SECONDS - tone_duration

    tone = create_sine_wave(duration_seconds=tone_duration)
    silence = np.zeros(int(silence_duration * SAMPLE_RATE), dtype=np.float32)

    audio = np.concatenate((tone, silence))
    stereo = to_stereo(audio)

    write_wav(OUTPUT_DIR / "defects" / "long_end_silence.wav", stereo)


def main() -> None:
    create_clean_sine()
    create_clipped_sine()
    create_silent_file()
    create_long_start_silence()
    create_long_end_silence()

    print("Synthetic test audio generated successfully.")


if __name__ == "__main__":
    main()