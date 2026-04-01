# EEG Analysis Checklist - Six-Problem Study

**Project Status**: ✅ Scripts Ready | ⏳ Awaiting EEG Data

---

## PRE-PROCESSING CHECKLIST

### Environment Setup ✅ COMPLETE
- [x] Python 3.x installed
- [x] MNE-Python (1.10.1) available
- [x] pandas library installed
- [x] openpyxl library installed
- [x] All scripts created and tested
- [x] Excel template ready (EEG_Segmentation.xlsx)

### Data Preparation ⏳ PENDING
- [ ] EEG files accessible on D: drive
- [ ] All subject folders present
- [ ] VHdr files present (±vmrk ±eeg companion files)
- [ ] File naming documented
- [ ] Backup of Excel file created

---

## PROCESSING CHECKLIST

### Step 1: Marker Extraction ⏳ PENDING
**Command**: `python analyze_eeg_batch.py`

**Pre-Processing**:
- [ ] Verify EEG files are accessible
- [ ] Check file formats (.vhdr, .edf, .set, .fif)
- [ ] Note any corrupted files

**During Processing**:
- [ ] Monitor console output for errors
- [ ] Check processing speed
- [ ] Look for any warnings

**Post-Processing**:
- [ ] Verify eeg_extracted_events.csv created
- [ ] Check file has entries for all subjects
- [ ] Review marker counts (expected ~38 per file)

### Step 2: Excel Population ⏳ PENDING
**Command**: `python fill_excel_from_eeg.py`

**Pre-Population**:
- [ ] Close EEG_Segmentation.xlsx in Excel
- [ ] Verify eeg_extracted_events.csv exists
- [ ] Check file naming matches Excel entries

**During Population**:
- [ ] Monitor console for match status
- [ ] Check for file name mismatches
- [ ] Note any rows that couldn't be updated

**Post-Population**:
- [ ] Verify EEG_Segmentation.xlsx updated
- [ ] Check backup file created
- [ ] Open Excel and review data

---

## VALIDATION CHECKLIST

### Marker Verification ⏳ PENDING
**File**: eeg_extracted_events.csv

For each file:
- [ ] Total_Events equals or close to 38
- [ ] Match_Status is "OK" or "MISMATCH"
- [ ] If MISMATCH: Review Unexpected_Markers and Missing_Markers
- [ ] All expected marker types present (eye_closed, 1_problem, etc.)
- [ ] No critical marker gaps

### Event Count Verification ⏳ PENDING
**File**: EEG_Segmentation.xlsx

For each subject:
- [ ] Column B (total_event): ~38
- [ ] Column C (match_or_not): Filled
- [ ] Column D (eye_closed): 1
- [ ] Columns E-J (Problem 1): All filled (6 markers)
- [ ] Columns K-P (Problem 2): All filled (6 markers)
- [ ] Columns Q-V (Problem 3): All filled (6 markers)
- [ ] Columns W-AB (Problem 4): All filled (6 markers)
- [ ] Columns AC-AH (Problem 5): All filled (6 markers)
- [ ] Columns AI-AN (Problem 6): All filled (6 markers)
- [ ] Last column (eye_closed_2): 1

**Validation Formulas** (Optional - Add to Excel):
```
=COUNTIF(D2:AN2,">0") should be ~36 (6 problems × 6 markers)
=SUM(D2:AN2) should be ~38 (all markers)
=IF(C2="OK","PASS","CHECK") for manual review
```

### Data Quality ⏳ PENDING
- [ ] No negative numbers in marker counts
- [ ] No values > 5 for any single marker (except eye_closed)
- [ ] Consistent data across all rows
- [ ] No blank cells in critical columns
- [ ] All numeric data proper format

---

## MISMATCH RESOLUTION CHECKLIST

### If Match_Status = "MISMATCH" ⏳ PENDING

**Investigation Steps**:
1. [ ] Open eeg_extracted_events.csv
2. [ ] Find row with MISMATCH status
3. [ ] Check "Unexpected_Markers" column
4. [ ] Check "Missing_Markers" column
5. [ ] Note the differences

**Common Issues**:

**Issue: Missing Markers**
- [ ] Check if trial was incomplete
- [ ] Verify with original recording software
- [ ] Document reason in notes
- [ ] Mark as "INCOMPLETE" if critical markers missing

**Issue: Unexpected Markers**
- [ ] List all unexpected marker names
- [ ] Check if they're alternate names
- [ ] Create mapping if pattern found
- [ ] Update script if consistent

**Issue: Total Count Wrong**
- [ ] Count should be 38 (±1-2 acceptable)
- [ ] If > 40: Likely duplicate markers
- [ ] If < 36: Missing events
- [ ] Manual review recommended

**Resolution**:
- [ ] Document findings in notes
- [ ] Update Match_Status in Excel if resolved
- [ ] Re-run script if mapping added
- [ ] Mark as verified

---

## DOCUMENTATION CHECKLIST

### Recording Findings ⏳ PENDING
- [ ] Create summary of mismatches
- [ ] Document marker name variations found
- [ ] Note any files with issues
- [ ] Record processing statistics

### Quality Report ⏳ PENDING
- [ ] Total files processed: ___
- [ ] Successful: ___ (% __)
- [ ] Mismatches: ___ (% __)
- [ ] Errors: ___
- [ ] Processing time: ___

### Final Documentation ⏳ PENDING
- [ ] Update PROGRESS_SUMMARY.md with actual results
- [ ] Add any new marker mappings found
- [ ] Document all issues and resolutions
- [ ] Create final validation report

---

## TROUBLESHOOTING CHECKLIST

### Script Errors ⏳ PENDING
If analyze_eeg_batch.py fails:
- [ ] Check if EEG files exist
- [ ] Verify file paths are correct
- [ ] Check if files are corrupted
- [ ] Review console error message
- [ ] Check if disk space available
- [ ] Verify MNE-Python installed

If fill_excel_from_eeg.py fails:
- [ ] Check if CSV file exists
- [ ] Verify Excel file not open
- [ ] Check if file names match
- [ ] Review console error message
- [ ] Ensure openpyxl installed

### Data Issues ⏳ PENDING
If marker counts don't match:
- [ ] Verify expected count is correct (should be 38)
- [ ] Check if trial was incomplete
- [ ] Review raw EEG file
- [ ] Look for duplicate events
- [ ] Check for missing segments

### Excel Issues ⏳ PENDING
If Excel won't open updated file:
- [ ] Close all Excel instances
- [ ] Check file isn't read-only
- [ ] Try opening backup first
- [ ] Check disk space
- [ ] Verify file format (.xlsx)

---

## SIGN-OFF CHECKLIST

### Ready for Analysis ✅ COMPLETE
- [x] All scripts created and tested
- [x] Documentation complete
- [x] Excel template ready
- [x] Environment verified
- [x] Expected marker structure documented

### Ready for Execution ⏳ PENDING
- [ ] EEG data accessible
- [ ] All paths verified
- [ ] Backup of original Excel created
- [ ] Team notified
- [ ] Contingency plan in place

### Post-Processing ⏳ PENDING
- [ ] All files processed
- [ ] Results verified
- [ ] Excel populated
- [ ] Quality report created
- [ ] Findings documented
- [ ] Team notified of completion

---

## TIMELINE

### Phase 1: Preparation ✅ COMPLETE
- [x] Analysis framework designed
- [x] Scripts created
- [x] Documentation prepared
- **Status**: Ready

### Phase 2: Execution ⏳ PENDING
- [ ] EEG data obtained
- [ ] Scripts run on full dataset
- [ ] Initial results reviewed
- **Estimated**: 1-2 hours (once data available)

### Phase 3: Validation ⏳ PENDING
- [ ] Results verified
- [ ] Mismatches resolved
- [ ] Excel finalized
- **Estimated**: 1-2 hours

### Phase 4: Documentation ⏳ PENDING
- [ ] Findings compiled
- [ ] Report generated
- [ ] Issues documented
- **Estimated**: 1 hour

---

## QUICK REFERENCE

### Commands
```bash
# Run marker extraction
cd C:\Users\whyke\github\six-problem\Data
python analyze_eeg_batch.py

# Run Excel update
python fill_excel_from_eeg.py

# View results
cat eeg_extracted_events.csv | head -5
```

### Expected Marker Count Per Subject
```
eye_closed:     1
1_problem:      1    1_solution:    1    1_rate:  2    1_eval:  1    1_type:  1
2_problem:      1    2_solution:    1    2_rate:  2    2_eval:  1    2_type:  1
3_problem:      1    3_solution:    1    3_rate:  2    3_eval:  1    3_type:  1
4_problem:      1    4_solution:    1    4_rate:  2    4_eval:  1    4_type:  1
5_problem:      1    5_solution:    1    5_rate:  2    5_eval:  1    5_type:  1
6_problem:      1    6_solution:    1    6_rate:  2    6_eval:  1    6_type:  1
eye_closed_2:   1
                                          TOTAL: 38 markers
```

### Excel Columns
- A: Name
- B: total_event
- C: match_or_not
- D: eye_closed
- E-J: Problem 1 events
- K-P: Problem 2 events
- Q-V: Problem 3 events
- W-AB: Problem 4 events
- AC-AH: Problem 5 events
- AI-AN: Problem 6 events
- AO: eye_closed_2

---

## NOTES

### Known Limitations
- PDF documentation is image-based (no OCR)
- Marker names must exactly match (case-sensitive)
- EEG files must be in supported format
- Requires access to D: drive for data

### Assumptions
- 38 markers per session is expected
- Marker names match Excel column headers
- Files named with subject ID for easy matching
- One recording per subject

### Dependencies
- MNE-Python 1.10.1 (for EEG reading)
- pandas (for data handling)
- openpyxl (for Excel manipulation)

---

## APPROVAL & SIGN-OFF

**Prepared By**: Claude Code  
**Preparation Date**: 2026-04-01  
**Status**: ✅ Ready for Execution

**Approver**: _________________  
**Approval Date**: _________________  
**Notes**: _________________

---

## APPENDIX: File Inventory

### Source Data
- [ ] EEG files: D:\Six problem\...\EEG_six_problem\
- [ ] Excel template: EEG_Segmentation.xlsx
- [ ] Reference PDF: Cognitive studies of design_experiment notebook.pdf

### Generated Files
- [ ] eeg_extracted_events.csv
- [ ] EEG_Segmentation.xlsx (updated)
- [ ] EEG_Segmentation.xlsx.backup_[timestamp]

### Documentation
- [x] TASK_GUIDE.md
- [x] README_EEG_ANALYSIS.md
- [x] PROGRESS_SUMMARY.md
- [x] CHECKLIST.md (this file)

### Scripts
- [x] analyze_eeg_markers.py
- [x] analyze_eeg_batch.py
- [x] fill_excel_from_eeg.py
- [x] extract_pdf_content.py

---

**Print this checklist and mark off items as you progress!**

✅ = Complete  
⏳ = Pending (awaiting data)  
🔄 = In Progress  
❌ = Blocked
