#!/usr/bin/env python3
"""Apply an avar v1, two-segment weight distribution to Metropolitan Line."""
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._a_v_a_r import table__a_v_a_r
import sys
from pathlib import Path

# The user-facing range is 400–900, but this deliberately exaggerates its
# distribution so the effect of avar v1 is obvious in a visual test:
#
#   400–600 → normalized design coordinates 0.0–0.1 (almost no change)
#   600–700 → normalized design coordinates 0.1–0.8 (rapid change)
#   700–900 → normalized design coordinates 0.8–1.0 (slow final change)
#
WEIGHT_MAP = [
    (400, 0.0),
    (600, 0.1),
    (700, 0.8),
    (900, 1.0),
]

if len(sys.argv) < 2:
    raise SystemExit(f"Usage: {Path(sys.argv[0]).name} INPUT.ttf [OUTPUT.ttf]")

input_path = Path(sys.argv[1])
output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else input_path.with_name(
    f"{input_path.stem}-avar1{input_path.suffix}"
)
font = TTFont(input_path)

weight_axis = next((axis for axis in font["fvar"].axes if axis.axisTag == "wght"), None)
if weight_axis is None:
    raise ValueError("The input font has no wght axis.")

if (weight_axis.minValue, weight_axis.defaultValue, weight_axis.maxValue) != (400, 400, 900):
    raise ValueError(
        "This test is defined for a wght axis with min/default/max values of 400/400/900."
    )

def normalize(value):
    """Normalize a user weight; the default equals the minimum in this font."""
    return (value - weight_axis.defaultValue) / (weight_axis.maxValue - weight_axis.defaultValue)

# Build segment dict: {fromCoordinate: toCoordinate}
segments = {-1.0: -1.0}  # Required avar v1 identity mapping, even if unreachable.
for weight, internal in WEIGHT_MAP:
    segments[normalize(weight)] = internal

# Create avar table
avar = table__a_v_a_r()
avar.segments = {'wght': segments}
# Explicitly write avar version 1.0 (not avar2's version 2.0).
avar.majorVersion = 1
avar.minorVersion = 0
font['avar'] = avar

print("Applied avar v1 exaggerated weight curve:")
for k, v in sorted(segments.items()):
    print(f"  wght {k:.3f} → internal {v:.3f}")

font.save(output_path)
print(f"Saved: {output_path}")
