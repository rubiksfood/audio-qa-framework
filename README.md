# Audio QA Framework

A Python-based Audio Quality Assurance Framework for validating audio files against configurable quality profiles.

## Goals

- Demonstrate audio QA methodology
- Automate repeatable technical checks
- Generate clear QA reports
- Combine audio analysis with structured QA documentation

## MVP Features

- WAV metadata validation
- Peak level detection
- Clipping detection
- Silence detection
- JSON and console reports
- pytest test coverage

## Generating Test Audio

Synthetic audio fixtures can be generated with:

```bash
python scripts/generate_test_audio.py
```

The generated files are used to test clipping detection, silence detection, and metadata validation.