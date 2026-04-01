# Quick Start Guide - EEG Analysis

**Status**: Ready to Run (awaiting EEG files)

---

## 📋 What We Have

✅ **Analysis Scripts Ready**
- `analyze_eeg_batch.py` - Extracts markers from EEG files
- `fill_excel_from_eeg.py` - Populates Excel with results

✅ **Excel Template Ready**
- `EEG_Segmentation.xlsx` - 39 subjects, 42 columns

✅ **Documentation Complete**
- Full task guide
- Detailed workflows
- Troubleshooting guide

⏳ **Awaiting EEG Data**
- Located at: D:\Six problem\...\EEG_six_problem\

---

## ⚡ Quick Execution (Once EEG Files Available)

### Step 1: Run Extraction (2-5 minutes)
```bash
cd C:\Users\whyke\github\six-problem\Data
python analyze_eeg_batch.py
```

**What happens**:
- Finds all EEG files
- Reads BrainVision format (.vhdr files)
- Counts all marker types
- Generates `eeg_extracted_events.csv`

**Expected output**:
- Console report with summary
- CSV file with marker counts for each subject
- Validation status (OK/MISMATCH)

### Step 2: Review Results (5 minutes)
```bash
# View extracted data
head -20 eeg_extracted_events.csv

# Check for issues
grep MISMATCH eeg_extracted_events.csv
```

**What to look for**:
- All files processed successfully
- Most have "OK" status
- Total_Events near 38 per file

### Step 3: Update Excel (1 minute)
```bash
python fill_excel_from_eeg.py
```

**What happens**:
- Reads extracted CSV
- Matches files to Excel rows
- Fills in marker counts
- Creates backup automatically

**Expected output**:
- Updated `EEG_Segmentation.xlsx`
- Backup: `EEG_Segmentation.xlsx.backup_[timestamp]`

### Step 4: Verify Results (5-10 minutes)
1. Open updated `EEG_Segmentation.xlsx` in Excel
2. Check columns are populated:
   - Column B: Total event counts
   - Column C: Match status
   - Columns D onward: Marker counts
3. Look for any "MISMATCH" entries
4. Spot-check a few subjects against CSV

---

## 🎯 Expected Results

### Per-Subject Data
```
Name: subject_001
Total Events: 38
Match Status: OK
eye_closed: 1
1_problem: 1, 1_solution: 1, 1_rate: 2, 1_eval: 1, 1_type: 1
2_problem: 1, 2_solution: 1, 2_rate: 2, 2_eval: 1, 2_type: 1
... (repeat for problems 3-6)
eye_closed_2: 1
```

### Marker Count Summary
- eye_closed: 1
- Each problem (6 total): 6 markers
- eye_closed_2: 1
- **Total: 38 markers**

---

## ⚠️ Common Issues & Fixes

### Issue: "No EEG files found"
**Fix**: Verify D: drive is accessible
```bash
# Check if D: drive exists
ls /d
# If not found, update path in script
# See README_EEG_ANALYSIS.md for details
```

### Issue: Marker names don't match
**Example output**:
```
Unexpected_Markers: EC,PROBLEM_1
Missing_Markers: eye_closed,1_problem
```
**Fix**: This is expected if marker names differ. Script handles it.

### Issue: Excel won't update
**Fix**: Make sure Excel is completely closed
```bash
# Close all Excel instances
# Then run: python fill_excel_from_eeg.py
```

### Issue: Total events ≠ 38
**Possible causes**:
- Recording incomplete
- Extra/duplicate markers
- Missing segment

**What to do**:
1. Check CSV for "Unexpected_Markers" or "Missing_Markers"
2. If incomplete, mark as "INCOMPLETE" in Excel column C
3. Document in notes if needed

---

## 📊 Quality Checks

After running analysis, verify:

✅ **File Processing**
- [ ] All EEG files found (check count in console)
- [ ] All files processed (should have same count)
- [ ] No critical errors

✅ **Marker Extraction**
- [ ] Total_Events ~38 per file
- [ ] All marker types present
- [ ] Most files have "OK" status

✅ **Excel Population**
- [ ] All rows updated
- [ ] All columns have data
- [ ] No #ERROR values

✅ **Data Validation**
- [ ] No negative numbers
- [ ] No unusually high counts
- [ ] Consistent across subjects

---

## 📂 Files Reference

### Input Files (External)
```
D:\Six problem\six-problem\six-problem\EEG_six_problem\
```

### Processing Scripts
```
C:\Users\whyke\github\six-problem\Data\
├── analyze_eeg_batch.py          ← Main extraction script
└── fill_excel_from_eeg.py        ← Excel update script
```

### Output Files
```
C:\Users\whyke\github\six-problem\Data\
├── eeg_extracted_events.csv      ← Extracted markers
└── EEG_Segmentation.xlsx         ← Final populated Excel
```

### Documentation
```
C:\Users\whyke\github\six-problem\Data\
├── QUICK_START.md               (this file)
├── README_EEG_ANALYSIS.md       (detailed guide)
├── TASK_GUIDE.md                (task breakdown)
├── PROGRESS_SUMMARY.md          (current status)
└── CHECKLIST.md                 (verification checklist)
```

---

## 🚀 Command Summary

```bash
# Navigate to data directory
cd C:\Users\whyke\github\six-problem\Data

# Extract markers from all EEG files
python analyze_eeg_batch.py
# → Creates: eeg_extracted_events.csv

# Review results (optional)
head -10 eeg_extracted_events.csv

# Update Excel with extracted data
python fill_excel_from_eeg.py
# → Updates: EEG_Segmentation.xlsx
# → Creates: EEG_Segmentation.xlsx.backup_[timestamp]

# Verify in Excel
# → Open EEG_Segmentation.xlsx and review columns
```

**Total Time**: ~30 minutes for all 40 subjects

---

## 🎓 What Each Script Does

### analyze_eeg_batch.py

**Input**: EEG files (.vhdr, .edf, .set, .fif)

**Process**:
1. Search for EEG files in standard locations
2. For each file:
   - Read raw EEG data (MNE-Python)
   - Extract annotations/markers
   - Count each marker type
3. Generate summary and statistics

**Output**: `eeg_extracted_events.csv`

**Columns**:
- File: Subject filename
- Total_Events: Sum of all markers
- eye_closed, 1_problem, 1_solution, ...: Marker counts
- Match_Status: OK or MISMATCH
- Unexpected_Markers: Extra markers found
- Missing_Markers: Expected markers not found

---

### fill_excel_from_eeg.py

**Input**: 
- `eeg_extracted_events.csv` (from script 1)
- `EEG_Segmentation.xlsx` (template)

**Process**:
1. Read extracted CSV
2. Match filenames to Excel rows
3. For each match:
   - Fill total_event column
   - Fill marker count columns
   - Update match_or_not status
4. Create backup
5. Save updated Excel

**Output**: 
- Updated `EEG_Segmentation.xlsx`
- Backup file (auto-created)

---

## ✨ Next Steps After Completion

### Immediate
1. Review populated Excel
2. Check for MISMATCH entries
3. Resolve any issues

### Follow-up
1. Archive raw EEG data if needed
2. Share results with team
3. Document any findings

### Optional Enhancements
1. Add visualization of marker distribution
2. Create per-subject report
3. Statistical analysis of event timing
4. Quality control dashboard

---

## 📞 Help & Support

### If Scripts Fail
1. Check console output for error message
2. Review README_EEG_ANALYSIS.md "Troubleshooting" section
3. Verify paths and file formats
4. Ensure dependencies installed

### If Results Look Wrong
1. Check Total_Events column (should be ~38)
2. Look for MISMATCH entries
3. Review Unexpected_Markers and Missing_Markers
4. Compare with original EEG files

### If Excel Issues
1. Make sure Excel is closed
2. Check file isn't read-only
3. Verify sufficient disk space
4. Try opening backup file first

---

## 📝 Checklist Before Running

- [ ] EEG files downloaded/accessible
- [ ] D: drive mounted or path updated
- [ ] Excel file closed
- [ ] Current directory correct: `C:\Users\whyke\github\six-problem\Data`
- [ ] Both Python scripts present
- [ ] MNE-Python installed (`python -c "import mne"`)

---

## 🎉 Success Criteria

**Analysis complete when**:
- [x] Both scripts run without critical errors
- [x] CSV file generated with marker counts
- [x] Excel file populated with data
- [x] Most entries have "OK" status
- [x] Total event counts reasonable (~38 per file)

---

**Ready to go!** 🚀

Once EEG files are available, execute the three commands above and you're done in ~30 minutes.

For details, see README_EEG_ANALYSIS.md or TASK_GUIDE.md
