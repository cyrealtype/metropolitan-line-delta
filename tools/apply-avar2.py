#!/usr/bin/env python3
"""Inject avar2 into built font"""
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._a_v_a_r import table__a_v_a_r
import sys

font = TTFont(sys.argv[1])

# Your non-linear curve, normalized 0-1
segments = {
    'wght': {
        0.0: 0.0,       # 400 → 400
        0.1: 0.02,      # 450 → 410
        0.2: 0.06,      # 500 → 430
        0.3: 0.12,      # 550 → 460
        0.4: 0.20,      # 600 → 500
        0.5: 0.32,      # 650 → 560
        0.6: 0.46,      # 700 → 630
        0.7: 0.62,      # 750 → 710
        0.8: 0.78,      # 800 → 790
        0.9: 0.92,      # 850 → 860
        1.0: 1.0,       # 900 → 900
    }
}

avar = table__a_v_a_r()
avar.majorVersion = 2
avar.segments = segments
font['avar'] = avar

font.save(sys.argv[1])
print("avar2 injected ✓")