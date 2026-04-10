# -*- coding: utf-8 -*-
"""
September Marker Validation Framework
Compare expected markers from notebooks against actual EEG extraction results
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Based on handwritten notebook data provided
SEPTEMBER_EXPECTED_MARKERS = {
    "Sep_18": {
        "expected_range": (3, 43),
        "expected_count": 41,
        "notes": "Eye closed 0:51-3:57, 6 problems with 6 markers each, eye closed at end"
    },
    "Sep_12_Anthropology": {
        "expected_range": (2, 40),
        "expected_count": 39,
        "notes": "Eye closed 0:00:30-0:03:30, 6 problems, eye closed at end"
    },
    "Sep_13": {
        "expected_range": (2, 41),
        "expected_count": 40,
        "notes": "Eye closed, 6 problems with 'done' markers, eye closed 1:12:18-1:15:18"
    },
    "Sep_13_2": {
        "expected_range": (2, 42),
        "expected_count": 41,
        "notes": "Eye closed, 6 problems with 'done' markers, eye closed 0:40:47-0:43:47"
    }
}

# Actual EEG extraction results
SEPTEMBER_ACTUAL_MARKERS = {
    "Sep_12(2)": {
        "actual_range": (4, 44),
        "actual_count": 41,
        "s14_count": 21,
        "s15_count": 20
    },
    "Sep_12": {
        "actual_range": (4, 46),
        "actual_count": 43,
        "s14_count": 22,
        "s15_count": 21
    },
    "Sep_13(2)": {
        "actual_range": (4, 46),
        "actual_count": 43,
        "s14_count": 22,
        "s15_count": 21
    },
    "Sep_13": {
        "actual_range": (4, 45),
        "actual_count": 42,
        "s14_count": 21,
        "s15_count": 21
    },
    "Sep_18": {
        "actual_range": (4, 47),
        "actual_count": 44,
        "s14_count": 22,
        "s15_count": 22
    }
}

def generate_marker_set(start, end):
    """Generate set of consecutive marker numbers"""
    return set(range(start, end + 1))

def analyze_discrepancies():
    """Compare expected vs actual marker sequences"""

    print("="*100)
    print("SEPTEMBER MARKER VALIDATION ANALYSIS")
    print("="*100)

    print("\n【KEY FINDING】")
    print("Expected markers from notebooks vs Actual markers from EEG extraction\n")

    # Mapping of expected to actual files
    mapping = {
        "Sep_18": "Sep_18",
        "Sep_12_Anthropology": "Sep_12(2)",
        "Sep_13": "Sep_13",
        "Sep_13_2": "Sep_13(2)"
    }

    for expected_name, actual_name in mapping.items():
        if expected_name not in SEPTEMBER_EXPECTED_MARKERS or actual_name not in SEPTEMBER_ACTUAL_MARKERS:
            continue

        expected = SEPTEMBER_EXPECTED_MARKERS[expected_name]
        actual = SEPTEMBER_ACTUAL_MARKERS[actual_name]

        exp_start, exp_end = expected['expected_range']
        act_start, act_end = actual['actual_range']

        exp_set = generate_marker_set(exp_start, exp_end)
        act_set = generate_marker_set(act_start, act_end)

        missing = exp_set - act_set
        extra = act_set - exp_set

        print(f"\n【{expected_name} → {actual_name}】")
        print(f"  Expected from notebook: {exp_start}-{exp_end} ({len(exp_set)} markers)")
        print(f"  Actual from EEG:        {act_start}-{act_end} ({len(act_set)} markers)")
        print(f"  S14 count: {actual['s14_count']}, S15 count: {actual['s15_count']}")

        if missing:
            print(f"  ⚠ Missing in EEG: {sorted(missing)}")
        if extra:
            print(f"  ℹ Extra in EEG: {sorted(extra)}")

        if not missing and not extra:
            print(f"  ✓ Perfect match!")

        print(f"  Notes: {expected['notes']}")

    print("\n" + "="*100)
    print("NEXT STEP: Cross-reference these findings with notebook timings and event descriptions")
    print("="*100)

if __name__ == "__main__":
    analyze_discrepancies()
