# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import pdfplumber

pdf_path = r'C:\Users\whyke\github\six-problem\Data\Cognitive studies of design_experiment notebook.pdf'

with pdfplumber.open(pdf_path) as pdf:
    total = len(pdf.pages)
    print(f'Total pages: {total}')
    has_text = 0
    for i, page in enumerate(pdf.pages[:10]):
        t = page.extract_text()
        if t and t.strip():
            has_text += 1
            print(f'Page {i+1}: HAS TEXT - {t[:150]}')
        else:
            print(f'Page {i+1}: [no extractable text - scanned image]')
    print(f'\nPages with text in first 10: {has_text}/10')
