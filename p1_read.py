# -*- coding: utf-8 -*-
"""P1: dump structure of 4 book reports"""
import sys, os
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import docx

base = r"g:\A工作中心\风险处置Commercial risk management\01_认知理论"
files = [
    "读书报告《危机应对的道与术》.docx",
    "读书报告《掘金》.docx",
    "读书报告《稳评指南》.docx",
    "读书报告《闪电战》.docx",
]

for fname in files:
    fpath = os.path.join(base, fname)
    if not os.path.exists(fpath):
        print(f"\n=== {fname} NOT FOUND ===")
        continue
    doc = docx.Document(fpath)
    paras = [p.text for p in doc.paragraphs if p.text.strip()]
    print(f"\n{'='*60}")
    print(f"=== {fname} ({len(paras)} paragraphs) ===")
    print(f"{'='*60}")
    for i, p in enumerate(paras):
        # Only show headings and first 60 chars
        if any(p.startswith(kw) for kw in ['第', '摘要', '结论', '目录', '1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.']):
            print(f"  [{i}] {p[:80]}")
        elif i < 20:
            print(f"  [{i}] {p[:80]}")
