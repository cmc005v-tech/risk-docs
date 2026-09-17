# -*- coding: utf-8 -*-
"""P0 修复：处理文件名差异"""
import os, shutil, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

base = r"g:\A工作中心\风险处置Commercial risk management"

fixes = [
    # (实际文件名, 目标目录, 规范命名)
    ("6.商业风控 \u2014 企业的隐形数字资产白皮书.docx",
     "01_认知理论", "商业风控白皮书.docx"),
    ("风险投资人选择初创企业和团队的五大标准.docx",
     "01_认知理论", "投资人五大标准.docx"),
    ("谈判沟通话术框架.docx",
     "03_实操模板", "模板-谈判话术框架.docx"),
    ("最高人民法院关于适用 \u300a中华人民共和国民法典\u300b有关担保制度的解释 - 中华人民共和国最高人民法院.pdf",
     "05_法规参考", "法规-民法典担保制度解释.pdf"),
]

for src_name, dst_dir, dst_name in fixes:
    src = os.path.join(base, src_name)
    dst = os.path.join(base, dst_dir, dst_name)
    if os.path.exists(src):
        shutil.move(src, dst)
        print(f"[FIX] OK  {src_name} -> {dst_dir}/{dst_name}")
    else:
        print(f"[FIX] MISS {src_name}")

# 验证最终状态
print("\n=== 最终目录结构 ===")
dirs = ["01_认知理论","02_学习规划","03_实操模板","04_评估工具","05_法规参考","06_岗位认知方法论","07_网站源码"]
for d in dirs:
    p = os.path.join(base, d)
    files = []
    for root, _, fnames in os.walk(p):
        files.extend(fnames)
    print(f"\n  {d}/ : {len(files)} files")
    for f in sorted(files):
        print(f"    - {f}")

print("\n=== 根目录残留 ===")
for f in sorted(os.listdir(base)):
    fp = os.path.join(base, f)
    if os.path.isfile(fp):
        print(f"  {f}")
