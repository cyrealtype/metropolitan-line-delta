#!/usr/bin/env python3
"""Apply non-linear weight avar to MetropolitanLine"""
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._a_v_a_r import table__a_v_a_r
import sys

WEIGHT_MAP = [
    (400, 0.0),
    (500, 0.1),
    (600, 0.2),
    (700, 0.75),
    (800, 0.90),
    (900, 1.0),
]

def normalize(value, min_val=400, max_val=900):
    return (value - min_val) / (max_val - min_val)

font = TTFont(sys.argv[1])

# Build segment dict: {fromCoordinate: toCoordinate}
segments = {}
for weight, internal in WEIGHT_MAP:
    segments[normalize(weight)] = internal

# Create avar table
avar = table__a_v_a_r()
avar.segments = {'wght': segments}
font['avar'] = avar

print("Applied non-linear weight curve:")
for k, v in sorted(segments.items()):
    print(f"  wght {k:.3f} → internal {v:.3f}")

output = sys.argv[2] if len(sys.argv) > 2 else sys.argv[1]
font.save(output)
print(f"Saved: {output}")