# -*- coding: utf-8 -*-
"""P1 Batch2 fix: career files from content/ subdir"""
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

SITE_DIR = r"g:\A工作中心\风险处置Commercial risk management\07_网站源码\risk-learning-site"
CONTENT_DIR = os.path.join(SITE_DIR, "content")

def to_html_from_md(paras):
    lines = []
    in_list = False
    for p in paras:
        p = p.strip()
        if not p: continue
        if p.startswith("# "):
            if in_list: lines.append('</ul>'); in_list = False
            lines.append(f'<h2>{p[2:]}</h2>')
        elif p.startswith("## "):
            if in_list: lines.append('</ul>'); in_list = False
            lines.append(f'<h3>{p[3:]}</h3>')
        elif p.startswith("### "):
            if in_list: lines.append('</ul>'); in_list = False
            lines.append(f'<h4>{p[4:]}</h4>')
        elif p.startswith("- ") or p.startswith("* "):
            if not in_list: lines.append('<ul>'); in_list = True
            lines.append(f'<li>{p[2:]}</li>')
        elif p.startswith(("第一，", "第二，", "第三，", "第四，")):
            if in_list: lines.append('</ul>'); in_list = False
            lines.append(f'<p><strong>{p[:3]}</strong>{p[3:]}</p>')
        elif p.startswith("> "):
            if in_list: lines.append('</ul>'); in_list = False
            lines.append(f'<blockquote><p>{p[2:]}</p></blockquote>')
        else:
            if in_list: lines.append('</ul>'); in_list = False
            lines.append(f'<p>{p}</p>')
    if in_list: lines.append('</ul>')
    html = '\n'.join(lines)
    html = html.replace('\\', '\\\\')
    html = html.replace('"', '\u300c')
    html = html.replace('"', '\u300d')
    html = html.replace("'", "\\'")
    html = html.replace('\n', '\\n')
    return html

career_files = [
    ("career-01-角色定位.md", "theory-career-01", "风险处置顾问的角色定位与职责维度",
     "入门", "W0", "风险处置顾问承担经营落地与风险把控双重职责。角色定位区别于律师、普通风控、审计，核心在于商业处置能力：能写方案、能算成本、能给决策。"),
    ("career-02-诊策行复四步法.md", "theory-career-02", "诊策行复四步法：风险处置的标准化流程",
     "进阶", "W3", "诊断-策略-行动-复盘四步法构成风险处置的标准化流程闭环。每一步有明确的输入输出和质量标准，是从碎片化经验走向体系化处置的核心方法论。"),
    ("career-03-T型技能与进阶.md", "theory-career-03", "T型技能树与L1-L3进阶地图",
     "进阶", "W0", "风险处置顾问需要T型技能结构：横向覆盖法律/财务/行业/沟通四大领域，纵向深耕处置方案撰写与谈判执行。L1-L3三级进阶地图明确每级能力要求与成长路径。"),
    ("career-04-四大思维模型.md", "theory-career-04", "四大思维模型：风险处置的底层认知框架",
     "高阶", "W10", "四大思维模型构成风险处置的底层认知框架：系统思维（看全局）、底线思维（守风险）、博弈思维（找均衡）、演化思维（看动态）。从道到术的认知升级路径。"),
]

insert_block = ""
for fname, aid, title, diff, week, summary in career_files:
    fpath = os.path.join(CONTENT_DIR, fname)
    if os.path.exists(fpath):
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        paras = [line.strip() for line in content.split('\n') if line.strip()]
        html = to_html_from_md(paras)
        print(f"  OK: {fname} ({len(paras)} lines, html: {len(html)} chars)")
        
        insert_block += f'    "{aid}": {{\n'
        insert_block += f'      "id": "{aid}",\n'
        insert_block += f'      "title": {json.dumps(title, ensure_ascii=False)},\n'
        insert_block += f'      "tags": {json.dumps([diff, week, "岗位认知", "职业画像"], ensure_ascii=False)},\n'
        insert_block += f'      "difficulty": "{diff}",\n'
        insert_block += f'      "week": "{week}",\n'
        insert_block += f'      "source": "商业风险处置顾问 2026-09",\n'
        insert_block += f'      "updated": "2026-09-17",\n'
        insert_block += f'      "section": "theory",\n'
        insert_block += f'      "subsection": "career",\n'
        insert_block += f'      "summary": {json.dumps(summary, ensure_ascii=False)},\n'
        insert_block += f'      "relatedIds": [],\n'
        insert_block += f'      "contentHtml": "{html}"\n'
        insert_block += "    },\n"
    else:
        print(f"  NOT FOUND: {fpath}")

# Insert into data-theory.js
theory_path = os.path.join(SITE_DIR, "data-theory.js")
with open(theory_path, "r", encoding="utf-8") as f:
    content = f.read()

close_pattern = "  }\n};"
if close_pattern in content:
    content = content.replace(close_pattern, insert_block + close_pattern)
    with open(theory_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"\n[OK] 4 career articles appended to data-theory.js")
    print(f"[OK] File size: {os.path.getsize(theory_path) / 1024:.1f} KB")
else:
    print("ERROR: closing pattern not found")
