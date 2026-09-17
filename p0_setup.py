# -*- coding: utf-8 -*-
"""P0 内容标准化执行脚本 — Python 版"""
import os, shutil, sys
# 强制 stdout 使用 UTF-8，避免终端 GBK 编码报错
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

base = r"g:\A工作中心\风险处置Commercial risk management"

# ── P0-1: 确认 7 目录 ──
dirs = [
    "01_认知理论",
    "02_学习规划",
    "03_实操模板",
    "04_评估工具",
    "05_法规参考",
    "06_岗位认知方法论",
    "07_网站源码",
]
for d in dirs:
    p = os.path.join(base, d)
    os.makedirs(p, exist_ok=True)
    print(f"[P0-1] OK: {d}")

# ── P0-2/3: 文件归类 + 重命名 ──
moves = [
    ("1.危机应对的道与术_读书报告.docx",            "01_认知理论", "读书报告《危机应对的道与术》.docx"),
    ("2.掘金_不良资产经营_读书报告.docx",             "01_认知理论", "读书报告《掘金》.docx"),
    ("3.重大决策社会稳定风险评估指南_读书报告.docx",   "01_认知理论", "读书报告《稳评指南》.docx"),
    ("4.黑天鹅_读书报告.docx",                       "01_认知理论", "读书报告《黑天鹅》.docx"),
    ("5.闪电战_AI时代上市公司舆情攻防实战手册_读书报告.docx", "01_认知理论", "读书报告《闪电战》.docx"),
    ("6.商业风控 企业的隐形数字资产白皮书.docx",       "01_认知理论", "商业风控白皮书.docx"),
    ("投资人尽调选项目团队的五项标准.docx",            "01_认知理论", "投资人五大标准.docx"),
    ("风险处置学习方案（学习计划+书单+全套模板）.docx", "02_学习规划", "风险处置学习方案.docx"),
    ("标准风险处置方案模板_三套预案版.docx",           "03_实操模板", "模板-风险处置方案.docx"),
    ("企业风险排查的风险评估报告模板.docx",            "03_实操模板", "模板-风险评估报告.docx"),
    ("项目结案复盘报告模板.docx",                     "03_实操模板", "模板-结案复盘报告.docx"),
    ("风险隔离与止损操作SOP.docx",                    "03_实操模板", "模板-隔离止损SOP.docx"),
    ("谈判沟通话术.docx",                             "03_实操模板", "模板-谈判话术框架.docx"),
    ("企业风险全面尽调清单.xlsx",                     "04_评估工具", "工具-风险尽调清单.xlsx"),
    ("风险损失测算模板.xlsx",                         "04_评估工具", "工具-损失测算.xlsx"),
    ("风险等级评估表.xlsx",                           "04_评估工具", "工具-风险等级评估.xlsx"),
    ("中央企业应急管理办法（征求意见稿）.pdf",         "05_法规参考", "法规-央企应急管理办法.pdf"),
    ("最高人民法院关于适用《中华人民共和国民法典》关干担保制度的解释 - 中华人民共和国最高人民法院.pdf",
     "05_法规参考", "法规-民法典担保制度解释.pdf"),
]

moved = 0
not_found = []
for src_name, dst_dir, dst_name in moves:
    src = os.path.join(base, src_name)
    dst = os.path.join(base, dst_dir, dst_name)
    if os.path.exists(src):
        shutil.move(src, dst)
        print(f"[P0-2] OK  {src_name} -> {dst_dir}/{dst_name}")
        moved += 1
    else:
        not_found.append(src_name)
        print(f"[P0-2] MISS {src_name}")

# 商业风险处置顾问.md（可能不存在）
advisor = os.path.join(base, "商业风险处置顾问.md")
if os.path.exists(advisor):
    dst = os.path.join(base, "06_岗位认知方法论", "商业风险处置顾问.md")
    shutil.move(advisor, dst)
    print("[P0-2] OK  商业风险处置顾问.md -> 06_岗位认知方法论/")
    moved += 1
else:
    print("[P0-2] SKIP 商业风险处置顾问.md 不存在")

# ── P0-4: 移动 risk-learning-site → 07_网站源码 ──
site_src = os.path.join(base, "risk-learning-site")
site_dst = os.path.join(base, "07_网站源码", "risk-learning-site")
if os.path.exists(site_src):
    if os.path.exists(site_dst):
        shutil.rmtree(site_dst)
    shutil.move(site_src, site_dst)
    print("[P0-4] OK  risk-learning-site -> 07_网站源码/")
else:
    print("[P0-4] SKIP risk-learning-site 不存在")

# ── P0-5: 创建 assets + 复制 xlsx ──
assets_dir = os.path.join(base, "07_网站源码", "risk-learning-site", "assets")
os.makedirs(assets_dir, exist_ok=True)
print(f"[P0-5] OK: assets/ 目录已创建")

xlsx_copies = [
    ("04_评估工具", "工具-风险尽调清单.xlsx"),
    ("04_评估工具", "工具-损失测算.xlsx"),
    ("04_评估工具", "工具-风险等级评估.xlsx"),
]
for sub, name in xlsx_copies:
    src = os.path.join(base, sub, name)
    dst = os.path.join(assets_dir, name)
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f"[P0-5] OK  {name} -> assets/")
    else:
        print(f"[P0-5] MISS {src}")

# ── 验证 ──
print("\n" + "=" * 60)
print("P0 验证结果")
print("=" * 60)
print(f"成功移动: {moved} 个文件")
if not_found:
    print(f"未找到: {len(not_found)} 个文件")
    for f in not_found:
        print(f"  - {f}")

print("\n目录结构:")
for d in dirs:
    p = os.path.join(base, d)
    files = []
    for root, _, fnames in os.walk(p):
        files.extend(fnames)
    print(f"  {d}/ : {len(files)} 个文件")
    for f in sorted(files):
        print(f"    - {f}")

# 检查根目录残留
print("\n根目录残留文件:")
root_files = [f for f in os.listdir(base) if os.path.isfile(os.path.join(base, f))]
for f in sorted(root_files):
    print(f"  - {f}")
