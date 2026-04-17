import pandas as pd
from pathlib import Path
import re

DATA_DIR = Path(r"C:\Users\whyke\github\six-problem\Data\output")

custom_order = [
    "april_2(3)", "april_4(1)", "april_4(2)", "april_8", "april_15", 
    "april_16(1)", "april_16(3)", "april_18(1)", "april_18(2)", "april_19(1)", 
    "april_19(2)", "april_2(1)", "april_22", "april_24", "aug_5", 
    "july_29", "july_30", "june_25", "sep_12(2)", "sep_12", 
    "sep_13(2)", "sep_13", "sep_18"
]

def parse_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    data = {}
    for line in lines:
        if line.startswith("Total events:"):
            data["total events"] = line.split(":")[1].strip()
            break
            
    in_table = False
    for line in lines:
        if "FULL EVENTS LIST" in line:
            in_table = True
            continue
        if "=====" in line and in_table:
            break
            
        if in_table:
            parts = line.split()
            if len(parts) >= 5 and "Stimulus/S" in line:
                event_num = parts[0]
                if len(parts) > 5:
                    label = " ".join(parts[5:])
                    if label:
                        data[label] = event_num
    return data

def generate(use_corr=False):
    rows = []
    
    headers = ['Subject/Date', 'total events', 'eye_closed_1']
    for p in range(1, 7):
        headers.extend([f'{p}_problem', f'{p}_solution', f'{p}_rate_1', f'{p}_eval', f'{p}_type', f'{p}_rate_2'])
    headers.append('eye_closed_2')
    
    for subject in custom_order:
        # Match "april_2(1)" -> "april_02(1)"
        base_name = re.sub(r'_(\d)(?!\d)', r'_0\1', subject)
        
        file_corr = DATA_DIR / f"{base_name}_output_full_corr.txt"
        file_reg = DATA_DIR / f"{base_name}_output_full.txt"
        
        target_file = None
        if use_corr and file_corr.exists():
            target_file = file_corr
        elif file_reg.exists():
            target_file = file_reg
            
        if target_file and target_file.exists():
            data = parse_txt(target_file)
            row = {'Subject/Date': subject}
            row.update(data)
            
            for k in list(row.keys()):
                if "sol_think" in k or "sol_draw" in k:
                    base = k.split("_")[0] + "_solution"
                    if base in row:
                        row[base] += f" / {row[k]}"
                    else:
                        row[base] = row[k]
                        
            rows.append(row)
        else:
            print(f"Warning: No valid txt file found for {subject} (tried {base_name})")
            
    df = pd.DataFrame(rows)
    for h in headers:
        if h not in df.columns:
            df[h] = ""
            
    final_df = df[headers]
    
    out_name = "sheet_corr.xlsx" if use_corr else "sheet.xlsx"
    out_path = DATA_DIR / out_name
    final_df.to_excel(out_path, index=False)
    print(f"Successfully saved {out_path}")

generate(use_corr=False)
generate(use_corr=True)
