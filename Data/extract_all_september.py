#!/usr/bin/env python3
"""
自动为5个September文件运行load_data.py并保存输出到文件
Automatically extract data for all 5 September files and save outputs
"""

import sys
import io
import subprocess
from pathlib import Path

# 设置UTF-8输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ============================================================================
# 5个September文件列表
# ============================================================================

SEPTEMBER_FILES = {
    "sep_12(2)": r"C:\Users\whyke\github\six-problem\Data\OneDrive_1_01-04-2026\eeg_sep_12(2)\sep_12(2).vhdr",
    "sep_12": r"C:\Users\whyke\github\six-problem\Data\OneDrive_1_01-04-2026\eeg_sep_12\sep_12.vhdr",
    "sep_13(2)": r"C:\Users\whyke\github\six-problem\Data\OneDrive_1_01-04-2026\eeg_sep_13(2)\sep_13(2).vhdr",
    "sep_13": r"C:\Users\whyke\github\six-problem\Data\OneDrive_1_01-04-2026\eeg_sep_13\sep_13.vhdr",
    "eeg_sep_18": r"C:\Users\whyke\github\six-problem\Data\OneDrive_1_01-04-2026\eeg_sep_18\eeg_sep_18.vhdr",
}

# ============================================================================
# 修改load_data.py并运行
# ============================================================================

def extract_and_save(filename, filepath):
    """为一个文件运行load_data.py并保存输出"""

    print(f"\n{'='*100}")
    print(f"Processing: {filename}")
    print(f"File: {filepath}")
    print(f"{'='*100}")

    # 修改load_data.py第10行
    load_data_path = Path(r"C:\Users\whyke\github\six-problem\Data\load_data.py")

    with open(load_data_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 找到第10行并修改
    for i, line in enumerate(lines):
        if i == 9:  # 第10行（0-indexed是9）
            lines[i] = f'file_path = r"{filepath}"\n'
            break

    # 写回文件
    with open(load_data_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print(f"✓ Modified line 10 in load_data.py")

    # 运行load_data.py并捕获输出
    try:
        result = subprocess.run(
            ["python", str(load_data_path)],
            cwd=r"C:\Users\whyke\github\six-problem\Data",
            capture_output=True,
            text=True,
            encoding='utf-8'
        )

        output = result.stdout
        if result.stderr:
            output += "\n[STDERR]\n" + result.stderr

        # 保存到文件
        output_filename = f"{filename}_output.txt"
        output_path = Path(r"C:\Users\whyke\github\six-problem\Data") / output_filename

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(output)

        print(f"✓ Output saved to: {output_filename}")
        print(f"✓ File size: {output_path.stat().st_size} bytes")

        # 打印关键信息到屏幕
        print("\n【Key Information】")
        for line in output.split('\n'):
            if 'Total annotations' in line or 'Stimulus/S' in line or 'Total events' in line:
                print(f"  {line}")

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# ============================================================================
# 主程序
# ============================================================================

def main():
    print("="*100)
    print("SEPTEMBER EEG DATA EXTRACTION - ALL 5 FILES")
    print("September EEG数据提取 - 全部5个文件")
    print("="*100)

    success_count = 0
    failed_count = 0

    for filename, filepath in SEPTEMBER_FILES.items():
        if extract_and_save(filename, filepath):
            success_count += 1
        else:
            failed_count += 1

    # 汇总
    print("\n" + "="*100)
    print("SUMMARY")
    print("="*100)
    print(f"✓ Successfully processed: {success_count}/{len(SEPTEMBER_FILES)}")
    print(f"❌ Failed: {failed_count}/{len(SEPTEMBER_FILES)}")
    print(f"\nOutput files saved in: C:\\Users\\whyke\\github\\six-problem\\Data\\")
    print(f"Files:")
    for filename in SEPTEMBER_FILES.keys():
        print(f"  - {filename}_output.txt")
    print("="*100)

if __name__ == "__main__":
    main()
