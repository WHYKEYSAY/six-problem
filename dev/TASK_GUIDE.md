# EEG Analysis Task Guide - Six-Problem Cognitive Study

## Overview
This document provides a detailed guide for completing EEG marker analysis for the six-problem cognitive study.

## Current Status

### Files Available
- [x] `Cognitive studies of design_experiment notebook.pdf` (94 pages, 36MB - image-based)
- [x] `load_data.py` (reference implementation)
- [x] `EEG_Segmentation.xlsx` (target output with 39 rows already)
- [x] `Six-problem_nasa_tlx.xlsx` (supporting data)

### Excel Structure Found
The `EEG_Segmentation.xlsx` file has the following columns:
```
Name | total_event | match_or_not | eye_closed | 
  1_problem | 1_solution | 1_rate | 1_eval | 1_type | 1_rate |
  2_problem | 2_solution | 2_rate | 2_eval | 2_type | 2_rate |
  3_problem | 3_solution | 3_rate | 3_eval | 3_type | 3_rate |
  4_problem | 4_solution | 4_rate | 4_eval | 4_type | 4_rate |
  5_problem | 5_solution | 5_rate | 5_eval | 5_type | 5_rate |
  6_problem | 6_solution | 6_rate | 6_eval | 6_type | 6_rate |
  eye_closed_2
```

This shows the expected structure: 6 problems, each with event types:
- problem: Problem presentation
- solution: Solution shown
- rate: Rating request
- eval: Evaluation/feedback
- type: Typing/response
- rate: Rating (appears twice per problem)

### Six-Problem Event Types Identified
Based on the Excel structure, the expected markers are:

1. **eye_closed**: Baseline with eyes closed (appears at start and end)
2. **{N}_problem**: Problem N presented (6 problems total)
3. **{N}_solution**: Solution for problem N shown
4. **{N}_rate**: Rating for problem N (appears twice - before and after eval)
5. **{N}_eval**: Evaluation/feedback for problem N
6. **{N}_type**: Typing/input for problem N

Where N = 1, 2, 3, 4, 5, 6

### EEG Data Location
Reference path from `load_data.py`:
```
D:\Six problem\six-problem\six-problem\EEG_six_problem\eeg_april_02(1)\april_2(1).vhdr
```

**Note**: EEG files not currently accessible. They appear to be on an external D: drive or separate storage.

## Tasks Breakdown

### TASK 1: Verify Markers Against Documentation
**Status**: Pending - Requires EEG file access

**Steps**:
1. Access EEG files from the expected location or alternate paths
2. Use MNE-Python (v1.10.1 available) to read BrainVision files
3. Extract annotations/markers from raw EEG data
4. Compare against expected marker list:
   - eye_closed, {1-6}_problem, {1-6}_solution, {1-6}_rate, {1-6}_eval, {1-6}_type

**Expected Outcomes**:
- List of mismatches between documentation and actual markers
- Confidence score for each EEG file
- Mapping of actual marker names to standardized names

**Code Reference**: `load_data.py` shows the pattern:
```python
raw = mne.io.read_raw_brainvision(file_path, preload=True)
events, event_id = mne.events_from_annotations(raw)
```

---

### TASK 2: Extract Event Counts
**Status**: Pending - Requires EEG file access

**For each EEG file:**
1. Load raw EEG data with MNE
2. Extract annotations/markers
3. Count occurrences of each marker type
4. Record in this format:

```
File: subject_name
Total Events: XX
Events by Type:
  eye_closed: X
  1_problem: X
  1_solution: X
  1_rate: X
  1_eval: X
  1_type: X
  ... (repeat for problems 2-6)
  eye_closed_2: X
```

**Batch Processing**: Use the provided `analyze_eeg_batch.py` script (to be created)

---

### TASK 3: Verify Markers Against Notebook Records
**Status**: Pending - Requires PDF analysis

**Required from PDF Analysis**:
1. Extract experimental protocol details
2. Expected marker sequence per trial
3. Timing information for each event
4. Any known deviations or exceptions

**Action Items**:
- Since PDF is image-based, may need OCR or manual review
- Focus on sections about experimental design and marker definitions

---

### TASK 4: Fill EEG_Segmentation.xlsx
**Status**: In Progress

**For each EEG file (39 rows total)**:
1. **Column: Name** - Subject ID or file name
2. **Column: total_event** - Sum of all event counts
3. **Column: match_or_not** - Y/N/? (verified against documentation)
4. **Columns: eye_closed** - Count of eye_closed markers at start
5. **Columns: {N}_problem through {N}_rate** - Event counts for each problem
6. **Column: eye_closed_2** - Count of eye_closed markers at end

---

### TASK 5: Test Batch Preprocessing Feasibility
**Status**: Pending

**Tests to perform** (once EEG files accessible):
1. Load multiple EEG files in sequence
2. Measure processing time per file
3. Check memory usage
4. Test error handling for corrupted files
5. Document any limitations

**Success Criteria**:
- All files load successfully
- Processing time < 5 minutes per file
- No memory issues with standard PC
- Clear error messages for problematic files

---

## Implementation Scripts

### Script 1: `analyze_eeg_batch.py` (To Create)
Process multiple EEG files and extract marker information.

```python
import mne
import pandas as pd
from pathlib import Path

# Scan for EEG files
# For each file:
#   - Read raw EEG
#   - Extract events
#   - Count event types
#   - Store in DataFrame
# Export results to CSV
```

### Script 2: `fill_excel_from_eeg.py` (To Create)
Automatically fill EEG_Segmentation.xlsx from extracted EEG data.

```python
import openpyxl
import pandas as pd

# Read extracted events CSV
# Map to Excel columns
# Write to EEG_Segmentation.xlsx
# Mark verification status
```

---

## How to Proceed

### Immediate Actions (No EEG Files Required)
1. [x] Analyze available documentation
2. [x] Understand Excel structure
3. [x] Define expected markers
4. [ ] Document expected marker sequence from PDF (if readable)
5. [ ] Create batch processing scripts

### When EEG Files Become Available
1. Transfer EEG files to accessible location
2. Run `analyze_eeg_batch.py` to extract markers
3. Verify markers match documentation
4. Run `fill_excel_from_eeg.py` to populate Excel
5. Manual verification of results
6. Document any mismatches or issues

---

## Data Dictionary

### Marker Types
| Code | Full Name | Description | Expected Count |
|------|-----------|-------------|-----------------|
| EC | eye_closed | Baseline with eyes closed | 1 (at start) |
| PROB | X_problem | Problem X presented | 1 per problem |
| SOL | X_solution | Solution for problem X | 1 per problem |
| RATE | X_rate | Rating for problem X | 2 per problem |
| EVAL | X_eval | Evaluation feedback | 1 per problem |
| TYPE | X_type | Typing/input response | Variable |
| EC2 | eye_closed_2 | Baseline with eyes closed | 1 (at end) |

### Event Sequence Per Problem
Expected sequence for each of 6 problems:
1. {N}_problem - Problem presented
2. {N}_type - User types solution
3. {N}_rate - User rates confidence (pre-solution)
4. {N}_solution - Correct solution shown
5. {N}_eval - Evaluation/feedback provided
6. {N}_rate - User rates again (post-evaluation)

Total per problem: 6 markers
Total for session: 1 (ec) + 6×6 (problems) + 1 (ec2) = 38 markers

---

## Troubleshooting

### Issue: EEG files not found
- Check if D: drive is accessible
- Look for alternative backup paths
- Check for .zip archives that need extraction

### Issue: Marker names don't match
- Check case sensitivity (uppercase vs lowercase)
- Look for prefixes/suffixes in actual markers
- Check for alternative naming conventions in documentation

### Issue: Event counts mismatch
- Verify the file wasn't partially recorded
- Check for aborted trials
- Look for duplicate or missing events

---

## Next Steps
Once EEG files are accessible:
1. Run `analyze_eeg_batch.py`
2. Review extracted markers
3. Compare with expected sequence
4. Document findings
5. Update Excel with results
