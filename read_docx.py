# -*- coding: utf-8 -*-
import sys, os
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import docx

base = r"g:\A工作中心\风险处置Commercial risk management\01_认知理论"
fname = "读书报告《黑天鹅》.docx"
fpath = os.path.join(base, fname)

doc = docx.Document(fpath)
for i, p in enumerate(doc.paragraphs):
    if p.text.strip():
        print(f"[{i}] {p.text}")
