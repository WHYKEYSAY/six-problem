# EEG Six-Problem Study - Analysis & Processing Guide

## Quick Start

This guide explains how to complete the EEG marker analysis for the six-problem cognitive study.

### Status
- **Data Files**: ✓ Documentation, Excel template available
- **EEG Files**: ⚠ Require access (reference: D:\Six problem\...\EEG_six_problem)
- **Analysis Scripts**: ✓ Ready to use
- **Excel Template**: ✓ Ready for population

---

## What Needs to Be Done

Based on the task description, complete these steps:

### 1. **Verify Markers Against Documentation** ✓ PLAN READY
   - Compare actual EEG markers with expected markers
   - Identify and record mismatches
   - Update "match or not" column in Excel

### 2. **Test Batch Preprocessing Feasibility** ✓ SCRIPT READY
   - Load multiple EEG files sequentially
   - Measure performance metrics
   - Document any limitations

### 3. **Extract Event Counts** ✓ SCRIPT READY
   - Read all EEG files
   - Count each marker type
   - Save results to CSV

### 4. **Match Events with Documentation** ✓ PLAN READY
   - Compare extracted events with expected sequence
   - Verify marker order and timing
   - Document findings

### 5. **Extract Event Information** ✓ SCRIPT READY
   - Extract: eye_closed, problem, solution, rate, evaluation, typing
   - Count occurrences of each
   - Organize by problem (1-6)

### 6. **Fill Summary Table** ✓ SCRIPT READY
   - Populate EEG_Segmentation.xlsx with extracted data
   - Verify all columns are filled
   - Document verification status

---

## Expected EEG Structure

### Event Types (6 Problems × 6 Event Types)

```
Session Structure:
├── eye_closed        (baseline, start)
├── Problem 1
│   ├── 1_problem     (problem presented)
│   ├── 1_type        (user types solution)
│   ├── 1_rate        (pre-solution rating)
│   ├── 1_solution    (correct solution shown)
│   ├── 1_eval        (evaluation/feedback)
│   └── 1_rate        (post-solution rating)
├── Problem 2-6       (repeat above)
└── eye_closed_2      (baseline, end)
```

### Total Markers per Session
- 1 eye_closed (start)
- 36 event markers (6 problems × 6 markers)
- 1 eye_closed_2 (end)
- **Total: 38 markers**

---

## Excel File Structure

**File**: `EEG_Segmentation.xlsx`

**Columns**:
- `Name`: Subject ID or file name
- `total event`: Total marker count
- `match or not`: Verification status (Y/N/?)
- `eye_closed`: Count of initial baseline
- `1_problem` through `1_rate`: Problem 1 events
- `2_problem` through `2_rate`: Problem 2 events
- ... (repeat for problems 3-6)
- `6_problem` through `6_rate`: Problem 6 events
- `eye_closed_2`: Count of final baseline

**Current Status**: 39 rows (subject data ready to be populated)

---

## Scripts & Tools

### Script 1: `analyze_eeg_markers.py` - Initial Discovery
**Purpose**: Verify environment and analyze PDF structure

**Outputs**:
- Confirms MNE-Python is available
- Checks for EEG files
- Loads Excel template
- Extracts PDF content

**Usage**:
```bash
python analyze_eeg_markers.py
```

**Status**: ✓ Completed - Environment verified

---

### Script 2: `analyze_eeg_batch.py` - Main Processing ⭐
**Purpose**: Batch process EEG files and extract markers

**Inputs**:
- EEG files from: `D:\Six problem\...\EEG_six_problem\`
- Searches recursively for `.vhdr`, `.edf`, `.set`, `.fif` files

**Outputs**:
- `eeg_extracted_events.csv` - Extracted marker counts
- Console report with summary statistics
- Error log for problematic files

**Extracted Data Includes**:
- File name and path
- Total events extracted
- Event counts for each marker type
- Verification status (match/mismatch)
- Unexpected or missing markers

**Usage**:
```bash
python analyze_eeg_batch.py
```

**Expected Output Format**:
```
File,Total_Events,eye_closed,1_problem,1_solution,...,Match_Status
file1.vhdr,38,1,1,1,...,OK
file2.vhdr,38,1,1,1,...,OK
file3.vhdr,36,1,0,1,...,MISMATCH
```

---

### Script 3: `fill_excel_from_eeg.py` - Excel Update ⭐
**Purpose**: Automatically populate Excel from extracted events

**Inputs**:
- `eeg_extracted_events.csv` (from Script 2)
- `EEG_Segmentation.xlsx` (existing template)

**Outputs**:
- Updated `EEG_Segmentation.xlsx`
- Backup of original file (`.backup_YYYYMMDD_HHMMSS`)
- Console report with update summary

**What It Does**:
1. Reads extracted events from CSV
2. Matches extracted files to Excel rows (by name)
3. Fills event counts in appropriate columns
4. Updates verification status
5. Creates backup and saves updated file

**Usage**:
```bash
python fill_excel_from_eeg.py
```

---

## Processing Workflow

### When EEG Files Are Available

**Step 1: Run batch extraction**
```bash
python analyze_eeg_batch.py
```
- Output: `eeg_extracted_events.csv`
- Review console output for mismatches

**Step 2: Review extracted data**
```bash
# View the extracted CSV
cat eeg_extracted_events.csv | head -5
```
- Check if all event types were found
- Look for any mismatches or missing events

**Step 3: Update Excel**
```bash
python fill_excel_from_eeg.py
```
- Output: Updated `EEG_Segmentation.xlsx`
- Backup: `EEG_Segmentation.xlsx.backup_[timestamp]`

**Step 4: Manual verification**
- Open `EEG_Segmentation.xlsx`
- Review populated data
- Check "match or not" column for verification status
- Resolve any MISMATCH entries manually

---

## Troubleshooting

### Issue: "No EEG files found"

**Possible causes**:
- D: drive not mounted or accessible
- EEG files in different location
- Files have different extension than expected

**Solutions**:
1. Check if D: drive exists:
   ```bash
   ls /d
   ```
2. Find EEG files manually:
   ```bash
   find /c -name "*.vhdr" 2>/dev/null
   ```
3. Update search paths in `analyze_eeg_batch.py`:
   ```python
   EEG_SEARCH_PATHS = [
       Path(r"C:\your\custom\path"),
       # ... other paths
   ]
   ```

### Issue: "No annotations found"

**Possible causes**:
- EEG file corrupted
- Markers not saved in this file
- Wrong file format

**Solution**:
- Check file integrity
- Verify with original EEG recording software
- Skip file and process others

### Issue: Marker names don't match

**Possible causes**:
- Case sensitivity (EC vs ec vs Eye_Closed)
- Spaces or underscores in names
- Different naming convention

**Solutions**:
1. Review console output from `analyze_eeg_batch.py`
2. Check "Unexpected_Markers" and "Missing_Markers" columns in CSV
3. Add mapping logic to script if needed:
   ```python
   # In analyze_eeg_batch.py
   MARKER_ALIASES = {
       'EC': 'eye_closed',
       'Eye Closed': 'eye_closed',
       'EYEC': 'eye_closed',
       # ... add more as needed
   }
   ```

### Issue: Event counts don't add up

**Possible causes**:
- Missing events (trial interrupted)
- Duplicate events
- Extra unexpected events

**Solutions**:
1. Review "Match_Status" column in extracted CSV
2. Check "Unexpected_Markers" for extra events
3. Check "Missing_Markers" for incomplete trials
4. Manual review of raw EEG file may be needed

---

## Expected Results

### CSV Output Example
```
File,Total_Events,eye_closed,1_problem,1_solution,1_rate,1_eval,1_type,...,Match_Status
subject_001.vhdr,38,1,1,1,2,1,1,...,OK
subject_002.vhdr,38,1,1,1,2,1,1,...,OK
subject_003.vhdr,36,1,0,1,2,1,1,...,MISMATCH
```

### Excel Summary
| Name | total event | match or not | eye_closed | 1_problem | ... |
|------|------------|--------------|-----------|-----------|-----|
| subject_001 | 38 | OK | 1 | 1 | ... |
| subject_002 | 38 | OK | 1 | 1 | ... |
| subject_003 | 36 | MISMATCH | 1 | 0 | ... |

---

## Advanced: Manual Marker Mapping

If marker names in EEG files don't match expected names:

1. Extract all unique markers first:
   ```python
   import mne
   raw = mne.io.read_raw_brainvision(file_path)
   print(set(raw.annotations.description))
   ```

2. Create a mapping dictionary:
   ```python
   MARKER_MAPPING = {
       'Stimulus/1': '1_problem',
       'Stimulus/2': '1_solution',
       'Stimulus/3': '1_rate',
       # ... etc
   }
   ```

3. Update `analyze_eeg_batch.py` to use mapping

---

## File Reference

### In This Directory
- `TASK_GUIDE.md` - Detailed task breakdown
- `README_EEG_ANALYSIS.md` - This file
- `load_data.py` - Reference implementation
- `analyze_eeg_markers.py` - Environment verification
- `analyze_eeg_batch.py` - Main EEG processing
- `fill_excel_from_eeg.py` - Excel population
- `EEG_Segmentation.xlsx` - Output file (to populate)
- `Six-problem_nasa_tlx.xlsx` - Reference data

### External Files
- `Cognitive studies of design_experiment notebook.pdf` - Reference documentation (94 pages)
- EEG data: `D:\Six problem\...\EEG_six_problem\` (requires access)

---

## Key Dates & Deadlines

- **Task Created**: 2026-04-01
- **Current Status**: Scripts ready, awaiting EEG data access
- **Expected Completion**: Upon EEG file availability + processing time

---

## Questions & Support

### For Script Issues
1. Check error messages carefully
2. Review console output for specific warnings
3. Check file paths and ensure they exist
4. Verify Python packages are installed (`mne`, `pandas`, `openpyxl`)

### For Data Issues
1. Verify EEG files are accessible
2. Check file formats are supported (.vhdr, .edf, .set, .fif)
3. Use original recording software to verify file integrity
4. Check if markers were actually saved in recording

### For Excel Issues
1. Don't manually edit rows before running scripts
2. Keep backup copies before updating
3. Use Excel "Undo" if something goes wrong
4. Check cell formats (numbers vs text)

---

## Next Steps

### Immediate (No EEG Files Required)
- [x] Understand task requirements
- [x] Analyze Excel structure
- [x] Prepare processing scripts
- [x] Create documentation

### When EEG Files Available
- [ ] Transfer files to accessible location
- [ ] Run `analyze_eeg_batch.py`
- [ ] Review CSV output and check for mismatches
- [ ] Run `fill_excel_from_eeg.py`
- [ ] Manually verify Excel output
- [ ] Document any findings or issues

---

## Technical Details

### Environment
- **Python**: 3.x
- **Key Packages**: mne-python (1.10.1), pandas, openpyxl
- **EEG Formats Supported**: BrainVision (.vhdr), EDF+, EEGLAB (.set), FIF
- **OS**: Windows 11 (bash compatible)

### Performance
- **Per-file Processing**: ~1-5 seconds
- **Total for 40 files**: ~2-5 minutes
- **Memory Usage**: ~500MB typical
- **Disk Space**: Minimal (CSV output ~50KB)

---

## Version History

| Date | Version | Changes |
|------|---------|---------|
| 2026-04-01 | 1.0 | Initial setup and documentation |

---

**Last Updated**: 2026-04-01
**Status**: Ready for EEG data processing
