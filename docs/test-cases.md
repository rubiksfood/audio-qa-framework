# Test Cases

## AQ-001: Valid WAV file

Steps:
1. Run validator on clean WAV file.

Expected:
- File passes all MVP checks.

## AQ-002: Clipped WAV file

Steps:
1. Run validator on clipped WAV file.

Expected:
- Clipping check fails.
- Severity: Critical.