from audioqa.loader import read_metadata

metadata = read_metadata("sample-audio/clean/test.wav")

print(metadata)
print(f"Duration: {metadata.duration_seconds:.2f}s")