# -*- coding: utf-8 -*-
import sys, re, os
sys.stdout.reconfigure(encoding='utf-8')

site_dir = r"g:\A工作中心\风险处置Commercial risk management\07_网站源码\risk-learning-site"
files = ['data-path.js','data-theory.js','data-tools.js','data-lab.js','data-cases.js','data-law.js']
total = 0
for f in files:
    content = open(os.path.join(site_dir, f), encoding='utf-8').read()
    # Count "id": "xxx" patterns (article ids)
    ids = re.findall(r'"id":\s*"([^"]+)"', content)
    print(f'{f}: {len(ids)} articles -> {ids}')
    total += len(ids)
print(f'\nTOTAL: {total} articles')
