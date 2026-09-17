# -*- coding: utf-8 -*-
"""P0.5: generate data-theory.js from black swan docx"""
import sys, os, re, json
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import docx

base = r"g:\A工作中心\风险处置Commercial risk management\01_认知理论"
out_dir = r"g:\A工作中心\风险处置Commercial risk management\07_网站源码\risk-learning-site"

doc = docx.Document(os.path.join(base, "读书报告《黑天鹅》.docx"))
paras = [p.text for p in doc.paragraphs if p.text.strip()]

# ── Article content ranges (verified paragraph indices) ──
# Art1: 定义与两种世界 = 摘要+第一部分+1.1-1.3
art1_paras = paras[15:45]
# Art2: 认知盲区 = 第二部分+第三部分+第四部分前半(杠铃/冗余/选择权)
art2_paras = paras[45:137]
# Art3: 识别脆弱性 = 第五部分
art3_paras = paras[137:155]
# Art4: 反脆弱框架 = 第六部分+结论核心
art4_paras = paras[155:176] + paras[198:216]
# Art5: 跨境物流 = 第七部分
art5_paras = paras[176:198]


def to_html(para_list):
    """Convert paragraph list to HTML string, JS-safe"""
    lines = []
    in_list = False
    for p in para_list:
        p = p.strip()
        if not p:
            continue
        # Skip meta lines
        if p.startswith(("报告人：", "目录", "《黑天鹅")) and not p.startswith("《黑天鹅》不是"):
            continue

        # Detect heading patterns
        if re.match(r'^第[一二三四五六七]部分[：:]', p):
            if in_list:
                lines.append('</ul>')
                in_list = False
            lines.append(f'<h2>{p}</h2>')
        elif re.match(r'^\d\.\d\s', p):
            if in_list:
                lines.append('</ul>')
                in_list = False
            lines.append(f'<h3>{p}</h3>')
        elif p.startswith("摘要") and len(p) < 5:
            if in_list:
                lines.append('</ul>')
                in_list = False
            lines.append('<h2>摘要</h2>')
        elif p.startswith("结论") and len(p) < 5:
            if in_list:
                lines.append('</ul>')
                in_list = False
            lines.append('<h2>结论</h2>')
        # Bold-prefixed patterns
        elif p.startswith(("第一，", "第二，", "第三，", "第四，")):
            if in_list:
                lines.append('</ul>')
                in_list = False
            lines.append(f'<p><strong>{p[:3]}</strong>{p[3:]}</p>')
        elif p.startswith(("脆弱的事物：", "强韧的事物：", "反脆弱的事物：")):
            if in_list:
                lines.append('</ul>')
                in_list = False
            parts = p.split("：", 1)
            lines.append(f'<p><strong>{parts[0]}：</strong>{parts[1]}</p>')
        elif p.startswith(("脆弱型业务：", "强韧型业务：", "反脆弱型业务：")):
            if in_list:
                lines.append('</ul>')
                in_list = False
            parts = p.split("：", 1)
            lines.append(f'<p><strong>{parts[0]}：</strong>{parts[1]}</p>')
        elif p.startswith(("安全端", "冒险端", "坚决不做：")):
            if in_list:
                lines.append('</ul>')
                in_list = False
            parts = p.split("：", 1)
            lines.append(f'<p><strong>{parts[0]}：</strong>{parts[1]}</p>')
        elif p.startswith(("核心认知：", "核心原则：", "核心逻辑：", "核心结构：", "核心洞察：", "核心区别：")):
            if in_list:
                lines.append('</ul>')
                in_list = False
            lines.append(f'<blockquote><p>{p}</p></blockquote>')
        elif p.startswith(("对企业风险管理的颠覆性启示", "对个人学习的启示",
                           "对企业决策的启示", "应对原则：")):
            if in_list:
                lines.append('</ul>')
                in_list = False
            lines.append(f'<p><strong>{p}</strong></p>')
        elif p.startswith(("识别你业务中的", "企业中的", "破除方法：")):
            if in_list:
                lines.append('</ul>')
                in_list = False
            lines.append(f'<p><strong>{p}</strong></p>')
        elif p.startswith(("事前：", "事中：", "事后：")):
            if in_list:
                lines.append('</ul>')
                in_list = False
            parts = p.split("：", 1)
            lines.append(f'<p><strong>{parts[0]}：</strong>{parts[1]}</p>')
        # List-like items (short items starting with specific markers)
        elif re.match(r'^(客户集中度|政策依赖性|供应链关键节点|杠杆与资金|声誉敏感度)[：:]', p):
            if not in_list:
                lines.append('<ul>')
                in_list = True
            lines.append(f'<li>{p}</li>')
        elif p.startswith(("《危机应对", "《掘金》", "《重大决策", "《黑天鹅》→")):
            if not in_list:
                lines.append('<ul>')
                in_list = True
            lines.append(f'<li>{p}</li>')
        elif any(p.startswith(kw) for kw in ['\u7528\u201c', '\u9009\u62e9\u4e00\u4e2a', '\u5efa\u7acb\u4e2a\u4eba', '\u5728\u56e2\u961f\u4e2d']):
            if not in_list:
                lines.append('<ul>')
                in_list = True
            lines.append(f'<li>{p}</li>')
        else:
            if in_list:
                lines.append('</ul>')
                in_list = False
            lines.append(f'<p>{p}</p>')

    if in_list:
        lines.append('</ul>')

    html = '\n'.join(lines)
    # JS string safety
    html = html.replace('\\', '\\\\')
    html = html.replace('"', '\u300c')  # " → 「
    html = html.replace('"', '\u300d')  # " → 」
    html = html.replace("'", "\\'")
    html = html.replace('\n', '\\n')
    return html


# ── Build 5 articles ──
articles_meta = [
    {
        "id": "theory-book04-01",
        "title": "黑天鹅的定义与两种世界：平均斯坦 vs 极端斯坦",
        "tags": ["进阶", "W11", "反脆弱", "黑天鹅"],
        "difficulty": "进阶", "week": "W11",
        "source": "读书报告《黑天鹅》2026-09",
        "updated": "2026-09-17",
        "section": "theory", "subsection": "anti-fragile",
        "summary": "黑天鹅事件同时满足三重条件：事前不可预测性、极端冲击性、事后可解释性。塔勒布用平均斯坦与极端斯坦的二元框架揭示，企业经营诸多维度属于极端斯坦，但普通风控模型却用平均斯坦思维管理风险，这是根本性的方法论错误。火鸡隐喻进一步说明历史经验外推的致命缺陷。",
        "relatedIds": ["theory-book04-02", "theory-book04-03"],
        "paras": art1_paras
    },
    {
        "id": "theory-book04-02",
        "title": "认知盲区与预测幻觉：从钟形曲线到杠铃策略",
        "tags": ["进阶", "W11", "反脆弱", "认知偏差"],
        "difficulty": "进阶", "week": "W11",
        "source": "读书报告《黑天鹅》2026-09",
        "updated": "2026-09-17",
        "section": "theory", "subsection": "anti-fragile",
        "summary": "五大认知陷阱（叙事谬误、证实谬误、沉默证据、游戏谬误、专家幻觉）让我们对黑天鹅视而不见。肥尾分布揭示极端事件远超正态分布预期。杠铃策略、冗余与选择权构成从预测转向准备的三大实操工具。",
        "relatedIds": ["theory-book04-01", "theory-book04-03"],
        "paras": art2_paras
    },
    {
        "id": "theory-book04-03",
        "title": "识别企业脆弱性：爆雷预警信号与级联失效分析",
        "tags": ["进阶", "W11", "反脆弱", "脆弱性扫描"],
        "difficulty": "进阶", "week": "W11",
        "source": "读书报告《黑天鹅》2026-09",
        "updated": "2026-09-17",
        "section": "theory", "subsection": "anti-fragile",
        "summary": "应对黑天鹅的第一步不是预测而是识别脆弱性。拖延成本在极端斯坦中呈指数级增长，级联失效可沿业务依赖图谱传导。通过脆弱性扫描框架找到关键节点，为其准备隔离机制。",
        "relatedIds": ["theory-book04-01", "theory-book04-04", "tools-method05"],
        "paras": art3_paras
    },
    {
        "id": "theory-book04-04",
        "title": "构建反脆弱框架：从风控思维到反脆弱型组织",
        "tags": ["高阶", "W11", "反脆弱", "组织架构"],
        "difficulty": "高阶", "week": "W11",
        "source": "读书报告《黑天鹅》2026-09",
        "updated": "2026-09-17",
        "section": "theory", "subsection": "anti-fragile",
        "summary": "从风控到反脆弱是根本性战略思维转换。风险共担原则要求决策者为后果负责。反脆弱型组织需分散决策权、容忍小失败、保持双轨业务结构。个人层面可构建技能、收入、认知、健康四维杠铃。",
        "relatedIds": ["theory-book04-03", "theory-book04-05", "tools-method01"],
        "paras": art4_paras
    },
    {
        "id": "theory-book04-05",
        "title": "跨境物流场景适配：极端斯坦下的反脆弱策略",
        "tags": ["高阶", "W12", "反脆弱", "跨境物流"],
        "difficulty": "高阶", "week": "W12",
        "source": "读书报告《黑天鹅》2026-09",
        "updated": "2026-09-17",
        "section": "theory", "subsection": "anti-fragile",
        "summary": "跨境物流天然属于极端斯坦。航线杠铃、客户结构杠铃、币种杠铃、合规杠铃构成四维反脆弱策略。以目的国政策突变为例，对比脆弱型与反脆弱型企业的不同应对路径。",
        "relatedIds": ["theory-book04-04", "theory-book04-03"],
        "paras": art5_paras
    }
]

# Generate HTML for each article
for art in articles_meta:
    art["contentHtml"] = to_html(art.pop("paras"))

# ── Build data-theory.js ──
subsections = [
    {"id": "crisis", "title": "危机处置思辨", "source": "读书报告《危机应对的道与术》", "status": "pending"},
    {"id": "npa", "title": "不良资产经营", "source": "读书报告《掘金》", "status": "pending"},
    {"id": "risk-assess", "title": "风险评估方法论", "source": "读书报告《稳评指南》", "status": "pending"},
    {"id": "anti-fragile", "title": "反脆弱与非常规风险", "source": "读书报告《黑天鹅》", "status": "active"},
    {"id": "public-opinion", "title": "舆情攻防", "source": "读书报告《闪电战》", "status": "pending"},
    {"id": "risk-asset", "title": "风控资产化", "source": "商业风控白皮书", "status": "pending"},
    {"id": "capital-view", "title": "资本视角", "source": "投资人五大标准", "status": "pending"},
    {"id": "career", "title": "岗位认知与职业画像", "source": "商业风险处置顾问", "status": "pending"}
]

js = "/* data-theory.js - 理论课堂数据 */\n"
js += "/* P0.5 试跑：已入站《黑天鹅》5 篇，其余子板块待 P1 批次入站 */\n\n"
js += "SITE_DATA.theory = {\n"
js += "  subsections: " + json.dumps(subsections, ensure_ascii=False, indent=4) + ",\n"
js += "  articles: {\n"

for i, art in enumerate(articles_meta):
    js += f'    "{art["id"]}": {{\n'
    for key in ["id", "title", "tags", "difficulty", "week", "source", "updated", "section", "subsection", "summary", "relatedIds"]:
        val = json.dumps(art[key], ensure_ascii=False)
        js += f'      "{key}": {val},\n'
    js += f'      "contentHtml": "{art["contentHtml"]}"\n'
    js += "    }" + ("," if i < len(articles_meta) - 1 else "") + "\n"

js += "  }\n};\n"

out_path = os.path.join(out_dir, "data-theory.js")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(js)

print(f"[OK] data-theory.js generated: {len(articles_meta)} articles")
print(f"[OK] File size: {os.path.getsize(out_path) / 1024:.1f} KB")
for a in articles_meta:
    html_len = len(a["contentHtml"])
    print(f"  {a['id']}: {a['title'][:30]}... (html: {html_len} chars)")
