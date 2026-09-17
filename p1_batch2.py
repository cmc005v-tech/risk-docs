# -*- coding: utf-8 -*-
"""P1 Batch2: whitepaper + investor + career -> data-theory.js append"""
import sys, os, re, json
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import docx

BASE = r"g:\A工作中心\风险处置Commercial risk management"
THEORY_DIR = os.path.join(BASE, "01_认知理论")
SITE_DIR = os.path.join(BASE, "07_网站源码", "risk-learning-site")

def read_docx(fname):
    fpath = os.path.join(THEORY_DIR, fname)
    if not os.path.exists(fpath):
        print(f"  NOT FOUND: {fpath}")
        return []
    doc = docx.Document(fpath)
    return [p.text for p in doc.paragraphs if p.text.strip()]

def to_html(para_list):
    lines = []
    in_list = False
    for p in para_list:
        p = p.strip()
        if not p: continue
        if p.startswith(("报告人：", "目录", "版权声明")) and len(p) < 80: continue
        if re.match(r'^第[一二三四五六七八九十]+章[：:\s]', p):
            if in_list: lines.append('</ul>'); in_list = False
            lines.append(f'<h2>{p}</h2>')
        elif re.match(r'^\d+\.\d+\s', p):
            if in_list: lines.append('</ul>'); in_list = False
            lines.append(f'<h3>{p}</h3>')
        elif p.startswith(("附录", "关键术语")) and len(p) < 30:
            if in_list: lines.append('</ul>'); in_list = False
            lines.append(f'<h2>{p}</h2>')
        elif p.startswith(("第一，", "第二，", "第三，", "第四，", "第五，")):
            if in_list: lines.append('</ul>'); in_list = False
            lines.append(f'<p><strong>{p[:3]}</strong>{p[3:]}</p>')
        elif p.startswith(("核心认知：", "核心原则：", "核心逻辑：", "核心主张：")):
            if in_list: lines.append('</ul>'); in_list = False
            lines.append(f'<blockquote><p>{p}</p></blockquote>')
        elif p.startswith(("提示：", "简单概括：")):
            if in_list: lines.append('</ul>'); in_list = False
            lines.append(f'<blockquote><p>{p}</p></blockquote>')
        elif any(p.startswith(kw) for kw in ['对企业', '对个人', '对在岗']):
            if in_list: lines.append('</ul>'); in_list = False
            lines.append(f'<p><strong>{p}</strong></p>')
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

def find_idx(paras, keyword, start=0):
    for i in range(start, len(paras)):
        if keyword in paras[i]:
            return i
    return -1

# ── 1. Whitepaper ──
print("Reading whitepaper...")
wp = read_docx("商业风控白皮书.docx")
print(f"  Whitepaper: {len(wp)} paragraphs")

# Find chapter boundaries
wp_abs = find_idx(wp, "核心主张")
if wp_abs < 0: wp_abs = find_idx(wp, "面向在岗")
if wp_abs < 0: wp_abs = 0
wp_ch1 = find_idx(wp, "第一章")
wp_ch2 = find_idx(wp, "第二章")
wp_ch3 = find_idx(wp, "第三章")
wp_ch4 = find_idx(wp, "第四章")
wp_ch5 = find_idx(wp, "第五章")
wp_ch6 = find_idx(wp, "第六章")
wp_ch7 = find_idx(wp, "第七章")
wp_appendix = find_idx(wp, "附录")
if wp_appendix < 0: wp_appendix = len(wp)

# Split into 7 chapters (merge intro with ch1)
wp_articles = []
chapter_ranges = [
    (wp_abs, wp_ch2, "theory-wp-01", "绪论与概念解构：风控隐形数字资产的定义", "入门", "W1",
     "商业风控是企业隐形数字资产。本章重新审视风控在企业经营中的定位，解构风控隐形数字资产的定义与四大特征（无形性、组织可沉淀性、可迭代复用、价值依附全过程），从岗位职责视角理解风控资产落地。"),
    (wp_ch2, wp_ch3, "theory-wp-02", "中外商业风控思维模式对比", "进阶", "W1",
     "从供给端、需求端、人才市场、企业生命周期四个维度对比中外风控业态差异。海外头部风控机构因长期前置护航企业成长而权威，非因服务百强而强大。对比启示在于思维革新而非制度照搬。"),
    (wp_ch3, wp_ch5, "theory-wp-03", "国内风控资产化的现实阻碍与转型范式", "进阶", "W6",
     "四重阻碍：认知层面（资产观念未建立）、组织层面（岗位权责与考核导向）、实践层面（知识依附个体）、行业环境（事件驱动采购习惯）。五大转型范式：认知、时序、组织、积累、价值边界。"),
    (wp_ch5, wp_ch7, "theory-wp-04", "产业观测与实践启示：风控资产化的数字载体", "进阶", "W6",
     "基于318座城市202个子行业观测数据，推导行业行为结论。数字化工具是载体而非资产本身，先更新认知梳理经验再选用数字化载体。对企业实践的渐进式推进建议。"),
    (wp_ch7, wp_appendix, "theory-wp-05", "总结与行业展望", "入门", "W13",
     "五条核心结论：风控是服务经营目标的隐形数字资产；国内经理人属损失触发式思维；中外对比重在借鉴底层思维；四重阻碍是转型起点；风控价值需理性看待不可神化。面向经理人的行动提示。"),
]

for start, end, aid, title, diff, week, summary in chapter_ranges:
    if start >= 0 and end > start:
        wp_articles.append({
            "id": aid, "title": title,
            "tags": [diff, week, "白皮书", "风控资产化"],
            "difficulty": diff, "week": week,
            "source": "商业风控白皮书 2026-09",
            "updated": "2026-09-17", "section": "theory", "subsection": "risk-asset",
            "summary": summary,
            "relatedIds": [],
            "paras": wp[start:end]
        })

print(f"  Whitepaper articles: {len(wp_articles)}")

# ── 2. Investor 5 Standards ──
print("Reading investor standards...")
inv = read_docx("投资人五大标准.docx")
print(f"  Investor standards: {len(inv)} paragraphs")

inv_articles = []
if len(inv) > 5:
    inv_articles.append({
        "id": "theory-inv-01",
        "title": "投资人选择初创企业和团队的五大标准：资本视角的风控启示",
        "tags": ["进阶", "W6", "资本视角", "投资人"],
        "difficulty": "进阶", "week": "W6",
        "source": "投资人五大标准 2026-09",
        "updated": "2026-09-17", "section": "theory", "subsection": "capital-view",
        "summary": "从风险投资人遴选初创企业的五大标准出发，提炼资本视角对风险处置顾问的启示：团队能力、市场空间、商业模式、风险管控、退出机制五个维度的评估逻辑可迁移到企业风险评估。",
        "relatedIds": ["theory-book02-01", "theory-wp-01"],
        "paras": inv
    })

# ── 3. Career (4 theory files) ──
print("Reading career files...")
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

career_articles = []
for fname, aid, title, diff, week, summary in career_files:
    fpath = os.path.join(SITE_DIR, fname)
    if os.path.exists(fpath):
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        paras = [line.strip() for line in content.split('\n') if line.strip()]
        career_articles.append({
            "id": aid, "title": title,
            "tags": [diff, week, "岗位认知", "职业画像"],
            "difficulty": diff, "week": week,
            "source": "商业风险处置顾问 2026-09",
            "updated": "2026-09-17", "section": "theory", "subsection": "career",
            "summary": summary,
            "relatedIds": [],
            "paras": paras
        })
        print(f"  {fname}: {len(paras)} lines")
    else:
        print(f"  NOT FOUND: {fname}")

# ── Combine all Batch2 articles ──
all_b2 = wp_articles + inv_articles + career_articles
print(f"\nBatch2 total: {len(all_b2)} articles")

# ── Read existing data-theory.js ──
theory_path = os.path.join(SITE_DIR, "data-theory.js")
with open(theory_path, "r", encoding="utf-8") as f:
    existing = f.read()

# Update subsections status
existing = existing.replace(
    '{"id": "risk-asset", "title": "\\u98ce\\u63a7\\u8d44\\u4ea7\\u5316", "source": "\\u5546\\u4e1a\\u98ce\\u63a7\\u767d\\u76ae\\u4e66", "status": "pending"}',
    '{"id": "risk-asset", "title": "\\u98ce\\u63a7\\u8d44\\u4ea7\\u5316", "source": "\\u5546\\u4e1a\\u98ce\\u63a7\\u767d\\u76ae\\u4e66", "status": "active"}'
)
existing = existing.replace(
    '{"id": "capital-view", "title": "\\u8d44\\u672c\\u89c6\\u89d2", "source": "\\u6295\\u8d44\\u4eba\\u4e94\\u5927\\u6807\\u51c6", "status": "pending"}',
    '{"id": "capital-view", "title": "\\u8d44\\u672c\\u89c6\\u89d2", "source": "\\u6295\\u8d44\\u4eba\\u4e94\\u5927\\u6807\\u51c6", "status": "active"}'
)
existing = existing.replace(
    '{"id": "career", "title": "\\u5c97\\u4f4d\\u8ba4\\u77e5\\u4e0e\\u804c\\u4e1a\\u753b\\u50cf", "source": "\\u5546\\u4e1a\\u98ce\\u9669\\u5904\\u7f6e\\u987e\\u95ee", "status": "pending"}',
    '{"id": "career", "title": "\\u5c97\\u4f4d\\u8ba4\\u77e5\\u4e0e\\u804c\\u4e1a\\u753b\\u50cf", "source": "\\u5546\\u4e1a\\u98ce\\u9669\\u5904\\u7f6e\\u987e\\u95ee", "status": "active"}'
)

# Insert new articles before the closing "  }\n};"
insert_block = ""
for art in all_b2:
    html = to_html(art.pop("paras"))
    art["contentHtml"] = html
    insert_block += f'    "{art["id"]}": {{\n'
    for key in ["id", "title", "tags", "difficulty", "week", "source", "updated", "section", "subsection", "summary", "relatedIds"]:
        val = json.dumps(art[key], ensure_ascii=False)
        insert_block += f'      "{key}": {val},\n'
    insert_block += f'      "contentHtml": "{html}"\n'
    insert_block += "    },\n"

# Find the closing pattern and insert before it
close_pattern = "  }\n};"
if close_pattern in existing:
    existing = existing.replace(close_pattern, insert_block + close_pattern)
else:
    # Try alternate pattern
    close_pattern = "  }\n};\n"
    if close_pattern in existing:
        existing = existing.replace(close_pattern, insert_block + close_pattern)
    else:
        print("ERROR: Could not find closing pattern in data-theory.js")
        sys.exit(1)

# Update header comment
existing = existing.replace(
    "/* P1 Batch1: 5 篇读书报告 x 5 篇 = 25 篇文章已入站 */",
    "/* P1 Batch1+Batch2: 25篇读书报告 + 5篇白皮书 + 1篇投资人 + 4篇岗位认知 = 35篇已入站 */"
)
existing = existing.replace(
    "/* 待入站: 白皮书(risk-asset) + 投资人五大标准(capital-view) + 岗位认知(career) */",
    "/* 待入站: 无（theory 板块全量完成） */"
)

with open(theory_path, "w", encoding="utf-8") as f:
    f.write(existing)

print(f"\n[OK] data-theory.js updated with Batch2")
print(f"[OK] File size: {os.path.getsize(theory_path) / 1024:.1f} KB")
for a in all_b2:
    print(f"  {a['id']}: {a['title'][:50]}...")
