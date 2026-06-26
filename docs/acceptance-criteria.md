# Acceptance Criteria

## WAV File

PASS:
- readable
- supported format
- expected sample rate
- expected channels

FAIL:
- corrupt file
- unsupported format
- unreadable file

## Clipping

PASS:
- no samples at or above digital full scale

FAIL:
- clipped samples detected