import pandas as pd
import re
from pathlib import Path

# Paths
DATA_DIR = Path(r"C:\Users\whyke\github\six-problem\Data")
CSV_PATH = DATA_DIR / "EEG_Segmentation_correction.csv"
OUTPUT_XLSX = DATA_DIR / "output" / "sheet.xlsx"

def normalize_name(name):
    """Normalize subject names (lowercase, no .xlsx, no leading zeros)"""
    if not name: return ""
    name = str(name).strip().lower().replace(".xlsx", "").replace(" ", "_")
    name = re.sub(r'([_\(])0(\d)', r'\1\2', name)
    name = re.sub(r'^0(\d)', r'\1', name)
    return name

def generate_sheet():
    if not CSV_PATH.exists():
        print(f"Error: Source CSV not found at {CSV_PATH}")
        return

    # Read the summary CSV
    # Column headers in CSV: Name, total event, match or not, eye_closed, 1_problem, 1_solution, 1_rate, 1_eval, 1_type, 1_rate...
    df = pd.read_csv(CSV_PATH, encoding='latin-1')
    
    # Selecting and formatting columns
    # We want Name, total event, and the task columns
    cols = df.columns.tolist()
    
    # Clean marker values: extract first number from "24(25)"
    def extract_first_num(val):
        if pd.isna(val): return ""
        match = re.search(r'(\d+)', str(val))
        return match.group(1) if match else str(val)

    # Task columns start from index 3
    task_cols = cols[3:]
    for col in task_cols:
        df[col] = df[col].apply(extract_first_num)
    
    # Also clean "total event" column
    df['total event'] = df['total event'].apply(extract_first_num)

    # Rename Name to Date/Subject
    df = df.rename(columns={'Name': 'Subject/Date', 'total event': 'total events'})

    # User's specific headers for the task columns (handling the rate repeat)
    headers = ['Subject/Date', 'total events', 'eye_closed_1']
    
    # Calculate problem headers
    for p in range(1, 7):
        headers.extend([f'{p}_problem', f'{p}_solution', f'{p}_rate', f'{p}_eval', f'{p}_type', f'{p}_rate'])
    
    headers.append('eye_closed_2')
    
    # Map the existing data to these headers (assuming order matches)
    final_df = df.iloc[:, [0, 1] + list(range(3, min(len(cols), len(headers) + 2)))]
    
    # Set the headers exactly as requested (truncating or padding if needed)
    final_df.columns = headers[:len(final_df.columns)]

    # Final touch: ensure Subject/Date is clean
    final_df['Subject/Date'] = final_df['Subject/Date'].apply(normalize_name)

    # Sort by subject name
    final_df = final_df.sort_values('Subject/Date')

    # Save to Excel
    try:
        final_df.to_excel(OUTPUT_XLSX, index=False)
        print(f"Summary sheet generated successfully at: {OUTPUT_XLSX}")
    except PermissionError:
        alt_xlsx = DATA_DIR / "output" / "sheet_updated.xlsx"
        final_df.to_excel(alt_xlsx, index=False)
        print(f"Permission denied on sheet.xlsx. Saved alternatively to: {alt_xlsx}")
if __name__ == "__main__":
    generate_sheet()
