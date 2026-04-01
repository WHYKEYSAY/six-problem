#!/usr/bin/env python3
"""Extract content from PDF notebook using pdfplumber"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

try:
    import pdfplumber

    pdf_path = "Cognitive studies of design_experiment notebook.pdf"

    print("Extracting PDF content...")
    print("=" * 80)

    with pdfplumber.open(pdf_path) as pdf:
        print(f"Total pages: {len(pdf.pages)}\n")

        # Extract text and tables from all pages
        for i, page in enumerate(pdf.pages):
            print(f"\n{'='*80}")
            print(f"PAGE {i+1}")
            print(f"{'='*80}\n")

            # Extract text
            text = page.extract_text()
            if text:
                print("TEXT:")
                print(text[:2000])  # First 2000 chars

            # Extract tables
            tables = page.extract_tables()
            if tables:
                print("\nTABLES:")
                for j, table in enumerate(tables):
                    print(f"\nTable {j+1}:")
                    for row in table[:10]:  # First 10 rows
                        print(row)

            if i >= 9:  # First 10 pages
                break

    print("\n" + "=" * 80)
    print("Extraction complete. Saving full text to pdf_text_full.txt...")

    # Save full text
    with pdfplumber.open(pdf_path) as pdf:
        with open("pdf_text_full.txt", "w", encoding="utf-8") as f:
            for i, page in enumerate(pdf.pages):
                f.write(f"\n{'='*80}\nPAGE {i+1}\n{'='*80}\n\n")
                text = page.extract_text()
                if text:
                    f.write(text + "\n")

                # Add tables
                tables = page.extract_tables()
                if tables:
                    f.write("\n[TABLES]\n")
                    for j, table in enumerate(tables):
                        f.write(f"\nTable {j+1}:\n")
                        for row in table:
                            f.write(str(row) + "\n")

    print("[OK] Full content saved to pdf_text_full.txt")

except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()
