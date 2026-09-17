# -*- coding: utf-8 -*-
"""P1 Batch: process 4 book reports -> data-theory.js (all 25 articles)"""
import sys, os, re, json
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import docx

BASE = r"g:\A工作中心\风险处置Commercial risk management"
THEORY_DIR = os.path.join(BASE, "01_认知理论")
OUT_DIR = os.path.join(BASE, "07_网站源码", "risk-learning-site")

def read_docx(fname):
    doc = docx.Document(os.path.join(THEORY_DIR, fname))
    return [p.text for p in doc.paragraphs if p.text.strip()]

def to_html(para_list):
    lines = []
    in_list = False
    for p in para_list:
        p = p.strip()
        if not p:
            continue
        if p.startswith(("报告人：", "目录")) and len(p) < 80:
            continue
        if re.match(r'^第[一二三四五六七八]部分[：:]', p):
            if in_list: lines.append('</ul>'); in_list = False
            lines.append(f'<h2>{p}</h2>')
        elif re.match(r'^\d\.\d\s', p):
            if in_list: lines.append('</ul>'); in_list = False
            lines.append(f'<h3>{p}</h3>')
        elif p.startswith("摘要") and len(p) < 5:
            if in_list: lines.append('</ul>'); in_list = False
            lines.append('<h2>摘要</h2>')
        elif p.startswith("结论") and len(p) < 5:
            if in_list: lines.append('</ul>'); in_list = False
            lines.append('<h2>结论</h2>')
        elif re.match(r'^第[一二三四五六]层[：:]', p):
            if in_list: lines.append('</ul>'); in_list = False
            parts = p.split("：", 1)
            lines.append(f'<p><strong>{parts[0]}：</strong>{parts[1] if len(parts)>1 else ""}</p>')
        elif re.match(r'^第[一二三四五]步[：:]', p):
            if in_list: lines.append('</ul>'); in_list = False
            parts = p.split("：", 1)
            lines.append(f'<p><strong>{parts[0]}：</strong>{parts[1] if len(parts)>1 else ""}</p>')
        elif p.startswith(("第一，", "第二，", "第三，", "第四，", "第五，")):
            if in_list: lines.append('</ul>'); in_list = False
            lines.append(f'<p><strong>{p[:3]}</strong>{p[3:]}</p>')
        elif p.startswith(("核心认知：", "核心原则：", "核心逻辑：", "核心结构：", "核心洞察：", "核心区别：", "核心主张：")):
            if in_list: lines.append('</ul>'); in_list = False
            lines.append(f'<blockquote><p>{p}</p></blockquote>')
        elif any(p.startswith(kw) for kw in ['对企业', '对个人学习', '对风险处置', '应对原则']):
            if in_list: lines.append('</ul>'); in_list = False
            lines.append(f'<p><strong>{p}</strong></p>')
        elif p.startswith(("事前：", "事中：", "事后：")):
            if in_list: lines.append('</ul>'); in_list = False
            parts = p.split("：", 1)
            lines.append(f'<p><strong>{parts[0]}：</strong>{parts[1]}</p>')
        elif p.startswith(("脆弱的事物", "强韧的事物", "反脆弱的事物")):
            if in_list: lines.append('</ul>'); in_list = False
            lines.append(f'<p>{p}</p>')
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

# ── Read all 4 reports ──
print("Reading book reports...")
r1 = read_docx("读书报告《危机应对的道与术》.docx")
r2 = read_docx("读书报告《掘金》.docx")
r3 = read_docx("读书报告《稳评指南》.docx")
r4 = read_docx("读书报告《闪电战》.docx")
print(f"  危机应对: {len(r1)} paras")
print(f"  掘金: {len(r2)} paras")
print(f"  稳评指南: {len(r3)} paras")
print(f"  闪电战: {len(r4)} paras")

# ── Define article splits ──
# Each: (id, title, tags, difficulty, week, subsection, summary, para_range)

def find_idx(paras, keyword, start=0):
    for i in range(start, len(paras)):
        if keyword in paras[i]:
            return i
    return -1

# Report 1: 危机应对 (140 paras)
# Part1:[6-20], Part2:[21-41], Part3:[42-70], Part4:[71-89], Part5:[90-end]
r1_p1s = find_idx(r1, "第一部分")
r1_p2s = find_idx(r1, "第二部分")
r1_p3s = find_idx(r1, "第三部分")
r1_p4s = find_idx(r1, "第四部分")
r1_p5s = find_idx(r1, "第五部分")
r1_conc = find_idx(r1, "结论")
r1_abs = find_idx(r1, "摘要")

articles_r1 = [
    {
        "id": "theory-book01-01",
        "title": "危机应对的核心框架：四个关键环节与微观适配",
        "tags": ["入门", "W1", "危机处置", "道与术"],
        "difficulty": "入门", "week": "W1",
        "source": "读书报告《危机应对的道与术》2026-09",
        "updated": "2026-09-17", "section": "theory", "subsection": "crisis",
        "summary": "本书围绕确定处置时机、确定关键救助者、进行损失分担、选择处置平台四个关键环节展开。八章内容按理论认知到危机类型到处置环节到改革启示递进，底层逻辑可跨场景适配到企业微观风险处置。",
        "relatedIds": ["theory-book01-02", "theory-book01-05"],
        "paras": r1[r1_abs:r1_p2s]
    },
    {
        "id": "theory-book01-02",
        "title": "风险预判的底层逻辑：信号监测与模式识别",
        "tags": ["入门", "W2", "危机处置", "风险预判"],
        "difficulty": "入门", "week": "W2",
        "source": "读书报告《危机应对的道与术》2026-09",
        "updated": "2026-09-17", "section": "theory", "subsection": "crisis",
        "summary": "风险预判需将经济正常循环置于首位，通过信号监测到模式识别的方法升级，构建企业风险监测仪表盘。预判的核心不是精确预测，而是建立系统性的风险感知能力。",
        "relatedIds": ["theory-book01-01", "theory-book01-03"],
        "paras": r1[r1_p2s:r1_p3s]
    },
    {
        "id": "theory-book01-03",
        "title": "止损的底层逻辑：逆周期操作与拖延成本",
        "tags": ["进阶", "W4", "危机处置", "止损"],
        "difficulty": "进阶", "week": "W4",
        "source": "读书报告《危机应对的道与术》2026-09",
        "updated": "2026-09-17", "section": "theory", "subsection": "crisis",
        "summary": "危机时期需要逆周期操作的非常态决策能力。保住核心功能优先于保住全部资产，拖延成本呈指数级增长。止损的关键是区分核心与非核心资产，果断剥离后者。",
        "relatedIds": ["theory-book01-02", "theory-book01-04"],
        "paras": r1[r1_p3s:r1_p4s]
    },
    {
        "id": "theory-book01-04",
        "title": "复盘的底层逻辑：从事后复盘到事前预防",
        "tags": ["进阶", "W5", "危机处置", "复盘"],
        "difficulty": "进阶", "week": "W5",
        "source": "读书报告《危机应对的道与术》2026-09",
        "updated": "2026-09-17", "section": "theory", "subsection": "crisis",
        "summary": "危机是推动改革的重要契机。案例学习是核心能力，通过历史案例提炼规律。从单纯事后复盘升级为事前预防机制，将风险经验沉淀为组织资产。",
        "relatedIds": ["theory-book01-03", "theory-book01-05"],
        "paras": r1[r1_p4s:r1_p5s]
    },
    {
        "id": "theory-book01-05",
        "title": "企业突发风险处置SOP：从四个关键环节到能力体系",
        "tags": ["进阶", "W5", "危机处置", "SOP"],
        "difficulty": "进阶", "week": "W5",
        "source": "读书报告《危机应对的道与术》2026-09",
        "updated": "2026-09-17", "section": "theory", "subsection": "crisis",
        "summary": "将四个关键环节转化为企业处置SOP四步法：风险识别与等级划分、确定处置主体与资源调配、损失评估与分担方案、处置平台选择与执行。个人能力体系分认知层、方法层、工具层三层构建。",
        "relatedIds": ["theory-book01-01", "theory-book01-04"],
        "paras": r1[r1_p5s:]
    },
]

# Report 2: 掘金 (262 paras)
r2_p1s = find_idx(r2, "第一部分")
r2_p2s = find_idx(r2, "第二部分")
r2_p3s = find_idx(r2, "第三部分")
r2_p4s = find_idx(r2, "第四部分")
r2_p5s = find_idx(r2, "第五部分")
r2_conc = find_idx(r2, "结论")
r2_abs = find_idx(r2, "摘要")

articles_r2 = [
    {
        "id": "theory-book02-01",
        "title": "不良资产经营的核心逻辑：在垃圾中找黄金",
        "tags": ["进阶", "W6", "不良资产", "掘金"],
        "difficulty": "进阶", "week": "W6",
        "source": "读书报告《掘金》2026-09",
        "updated": "2026-09-17", "section": "theory", "subsection": "npa",
        "summary": "不良资产经营的本质是在垃圾中找黄金。行业经历从捡破烂到投行化的转型，五方博弈格局下价值链重构。企业微观视角：你的客户可能就是不良资产，需要识别并主动处置。",
        "relatedIds": ["theory-book02-02", "theory-book02-05"],
        "paras": r2[r2_abs:r2_p2s]
    },
    {
        "id": "theory-book02-02",
        "title": "尽职调查与估值：风险识别的手术刀",
        "tags": ["进阶", "W7", "不良资产", "尽调估值"],
        "difficulty": "进阶", "week": "W7",
        "source": "读书报告《掘金》2026-09",
        "updated": "2026-09-17", "section": "theory", "subsection": "npa",
        "summary": "尽调三维度：财务、法律、业务，构成风险识别的核心工具。估值方法从静态定价到动态增值，关键是在不确定性中找到价值基准点。",
        "relatedIds": ["theory-book02-01", "theory-book02-03"],
        "paras": r2[r2_p2s:r2_p3s]
    },
    {
        "id": "theory-book02-03",
        "title": "不良资产化解实操路径：从收购转让到破产重整",
        "tags": ["进阶", "W7", "不良资产", "处置路径"],
        "difficulty": "进阶", "week": "W7",
        "source": "读书报告《掘金》2026-09",
        "updated": "2026-09-17", "section": "theory", "subsection": "npa",
        "summary": "五大实操路径：收购转让（经典模式）、资产证券化（创新工具）、债务重组（续命术）、破产重整（最后出口）、债转股（身份转换）。每种路径适用场景与风险收益特征各异。",
        "relatedIds": ["theory-book02-02", "theory-book02-04"],
        "paras": r2[r2_p3s:r2_p4s]
    },
    {
        "id": "theory-book02-04",
        "title": "企业债务纾困方案设计：从诊断到交易结构",
        "tags": ["高阶", "W8", "不良资产", "方案设计"],
        "difficulty": "高阶", "week": "W8",
        "source": "读书报告《掘金》2026-09",
        "updated": "2026-09-17", "section": "theory", "subsection": "npa",
        "summary": "企业债务纾困五步法：风险诊断与等级划分、利益相关方分析、多预案推演、交易结构设计、执行与监督。配套成本测算模型与交易结构案例模板，是方案能力的核心训练。",
        "relatedIds": ["theory-book02-03", "theory-book02-05"],
        "paras": r2[r2_p4s:r2_p5s]
    },
    {
        "id": "theory-book02-05",
        "title": "行业趋势与个人能力建设：从道到器三层进阶",
        "tags": ["进阶", "W9", "不良资产", "能力建设"],
        "difficulty": "进阶", "week": "W9",
        "source": "读书报告《掘金》2026-09",
        "updated": "2026-09-17", "section": "theory", "subsection": "npa",
        "summary": "不良资产行业从捡破烂走向投行化。个人能力建设分三层：认知层（道）、方法层（术）、工具层（器）。结合跨境物流业务场景，风险处置顾问需要体系化能力而非碎片化经验。",
        "relatedIds": ["theory-book02-01", "theory-book02-04"],
        "paras": r2[r2_p5s:]
    },
]

# Report 3: 稳评指南 (248 paras)
r3_p1s = find_idx(r3, "第一部分")
r3_p2s = find_idx(r3, "第二部分")
r3_p3s = find_idx(r3, "第三部分")
r3_p4s = find_idx(r3, "第四部分")
r3_p5s = find_idx(r3, "第五部分")
r3_p6s = find_idx(r3, "第六部分")
r3_conc = find_idx(r3, "结论")
r3_abs = find_idx(r3, "摘要")

articles_r3 = [
    {
        "id": "theory-book03-01",
        "title": "稳评制度框架与核心认知：四性评估与五步工作法",
        "tags": ["入门", "W1", "风险评估", "稳评"],
        "difficulty": "入门", "week": "W1",
        "source": "读书报告《稳评指南》2026-09",
        "updated": "2026-09-17", "section": "theory", "subsection": "risk-assess",
        "summary": "稳评制度自下而上生长并最终制度化。四性评估框架（合法性、合理性、可行性、可控性）是底层逻辑，五步工作法（识别-分析-评级-防控-备案）是标准化流程。",
        "relatedIds": ["theory-book03-02", "theory-book03-04"],
        "paras": r3[r3_abs:r3_p2s]
    },
    {
        "id": "theory-book03-02",
        "title": "标准化风险识别方法：多维扫描与数智化赋能",
        "tags": ["入门", "W2", "风险评估", "风险识别"],
        "difficulty": "入门", "week": "W2",
        "source": "读书报告《稳评指南》2026-09",
        "updated": "2026-09-17", "section": "theory", "subsection": "risk-assess",
        "summary": "风险识别需多维度扫描：资料分析、实地走访、问卷调查、专家咨询、利益相关者分析。标准化构建风险因素清单，大数据与AI赋能实现数智化风险识别。",
        "relatedIds": ["theory-book03-01", "theory-book03-03"],
        "paras": r3[r3_p2s:r3_p3s]
    },
    {
        "id": "theory-book03-03",
        "title": "风险评级体系：三级划分与评估矩阵",
        "tags": ["入门", "W3", "风险评估", "风险评级"],
        "difficulty": "入门", "week": "W3",
        "source": "读书报告《稳评指南》2026-09",
        "updated": "2026-09-17", "section": "theory", "subsection": "risk-assess",
        "summary": "风险等级三级划分（高/中/低），风险评估矩阵量化概率与影响，一票否决机制守住底线，动态风险等级调整适应变化。评级是连接识别与处置的关键枢纽。",
        "relatedIds": ["theory-book03-02", "theory-book03-04"],
        "paras": r3[r3_p3s:r3_p4s]
    },
    {
        "id": "theory-book03-04",
        "title": "风险评估流程标准化与处置应对机制",
        "tags": ["进阶", "W4", "风险评估", "流程标准化"],
        "difficulty": "进阶", "week": "W4",
        "source": "读书报告《稳评指南》2026-09",
        "updated": "2026-09-17", "section": "theory", "subsection": "risk-assess",
        "summary": "评估程序标准化步骤、公众参与与利益相关者沟通、专家评审机制、评估报告编制规范。处置应对三早原则（早发现早处置早化解）、分级分类响应、应急处置预案。",
        "relatedIds": ["theory-book03-03", "theory-book03-05"],
        "paras": r3[r3_p4s:r3_p6s]
    },
    {
        "id": "theory-book03-05",
        "title": "企业微观适配：重大项目与合作的稳评应用",
        "tags": ["进阶", "W5", "风险评估", "企业适配"],
        "difficulty": "进阶", "week": "W5",
        "source": "读书报告《稳评指南》2026-09",
        "updated": "2026-09-17", "section": "theory", "subsection": "risk-assess",
        "summary": "将稳评方法论降维适配企业场景：重大项目立项前的风险评估、商业合作谈判前的尽职调查、投资决策前的风险研判。补齐标准化方案撰写能力，从政府决策延伸到企业治理。",
        "relatedIds": ["theory-book03-01", "theory-book03-04"],
        "paras": r3[r3_p6s:]
    },
]

# Report 4: 闪电战 (256 paras)
r4_p1s = find_idx(r4, "第一部分")
r4_p2s = find_idx(r4, "第二部分")
r4_p3s = find_idx(r4, "第三部分")
r4_p4s = find_idx(r4, "第四部分")
r4_p5s = find_idx(r4, "第五部分")
r4_p6s = find_idx(r4, "第六部分")
r4_conc = find_idx(r4, "结论")
r4_abs = find_idx(r4, "摘要")

articles_r4 = [
    {
        "id": "theory-book05-01",
        "title": "AI时代舆情生态重构：从黄金四小时到毫秒裂变",
        "tags": ["进阶", "W12", "舆情攻防", "闪电战"],
        "difficulty": "进阶", "week": "W12",
        "source": "读书报告《闪电战》2026-09",
        "updated": "2026-09-17", "section": "theory", "subsection": "public-opinion",
        "summary": "AI时代舆情规则彻底改写：黄金四小时法则失效，毫秒级裂变成为常态。舆情战场三重叠加效应，五大新型AI武器（AIGC武器化、深度伪造、算法投喂、社交机器人、数字幽灵）重塑攻防格局。",
        "relatedIds": ["theory-book05-02", "theory-book05-03"],
        "paras": r4[r4_abs:r4_p2s]
    },
    {
        "id": "theory-book05-02",
        "title": "舆情危机识别与预警：从单点监测到立体雷达",
        "tags": ["进阶", "W12", "舆情攻防", "风险预警"],
        "difficulty": "进阶", "week": "W12",
        "source": "读书报告《闪电战》2026-09",
        "updated": "2026-09-17", "section": "theory", "subsection": "public-opinion",
        "summary": "风险全域排查从单点监测升级为立体雷达体系。风险分级预警机制实现精准响应，以AI对抗AI的技术赋能监测与预警，构建企业舆情免疫系统。",
        "relatedIds": ["theory-book05-01", "theory-book05-03"],
        "paras": r4[r4_p2s:r4_p3s]
    },
    {
        "id": "theory-book05-03",
        "title": "黄金响应机制：危机爆发时的四小时实战拆解",
        "tags": ["高阶", "W12", "舆情攻防", "应急响应"],
        "difficulty": "高阶", "week": "W12",
        "source": "读书报告《闪电战》2026-09",
        "updated": "2026-09-17", "section": "theory", "subsection": "public-opinion",
        "summary": "黄金4小时实战拆解：第1小时快速确认抢占定义权、第2小时精准研判制定回应策略、第3小时统一口径全员封口、第4小时对外发声抢占叙事。态度优先于事实，唯一发言人制度。",
        "relatedIds": ["theory-book05-02", "theory-book05-04"],
        "paras": r4[r4_p3s:r4_p4s]
    },
    {
        "id": "theory-book05-04",
        "title": "负面风险处置与危机公关止损：从灭火到止损",
        "tags": ["高阶", "W12", "舆情攻防", "声誉修复"],
        "difficulty": "高阶", "week": "W12",
        "source": "读书报告《闪电战》2026-09",
        "updated": "2026-09-17", "section": "theory", "subsection": "public-opinion",
        "summary": "三重诊断法（溯源、情绪、事实）精准定位危机根源。法律手段攻防兼备，以AI对抗AI的攻防技术。从灭火到止损的思维转换，化危为机实现品牌重塑，复盘精进构建免疫资产。",
        "relatedIds": ["theory-book05-03", "theory-book05-05"],
        "paras": r4[r4_p4s:r4_p6s]
    },
    {
        "id": "theory-book05-05",
        "title": "跨境物流舆情风险处置：非上市企业的特殊适配",
        "tags": ["高阶", "W12", "舆情攻防", "跨境物流"],
        "difficulty": "高阶", "week": "W12",
        "source": "读书报告《闪电战》2026-09",
        "updated": "2026-09-17", "section": "theory", "subsection": "public-opinion",
        "summary": "非上市企业舆情特殊性：信息不透明但影响同样致命。跨境物流四大舆情风险：国际政治化、长链条归因难、跨文化沟通、社交媒体放大。实操框架覆盖事前预防、事中响应、事后修复。",
        "relatedIds": ["theory-book05-01", "theory-book05-04"],
        "paras": r4[r4_p6s:]
    },
]

# ── Combine all articles ──
all_new_articles = articles_r1 + articles_r2 + articles_r3 + articles_r4
print(f"\nTotal new articles: {len(all_new_articles)}")

# ── Read existing data-theory.js to preserve 黑天鹅 articles ──
existing_theory_path = os.path.join(OUT_DIR, "data-theory.js")
with open(existing_theory_path, "r", encoding="utf-8") as f:
    existing_content = f.read()

# Extract 黑天鹅 articles (theory-book04-01 to 05) from existing file
import re as re_mod
# We'll keep the existing 黑天鹅 articles and add new ones

# ── Build subsections ──
subsections = [
    {"id": "crisis", "title": "危机处置思辨", "source": "读书报告《危机应对的道与术》", "status": "active"},
    {"id": "npa", "title": "不良资产经营", "source": "读书报告《掘金》", "status": "active"},
    {"id": "risk-assess", "title": "风险评估方法论", "source": "读书报告《稳评指南》", "status": "active"},
    {"id": "anti-fragile", "title": "反脆弱与非常规风险", "source": "读书报告《黑天鹅》", "status": "active"},
    {"id": "public-opinion", "title": "舆情攻防", "source": "读书报告《闪电战》", "status": "active"},
    {"id": "risk-asset", "title": "风控资产化", "source": "商业风控白皮书", "status": "pending"},
    {"id": "capital-view", "title": "资本视角", "source": "投资人五大标准", "status": "pending"},
    {"id": "career", "title": "岗位认知与职业画像", "source": "商业风险处置顾问", "status": "pending"}
]

# ── Generate data-theory.js ──
js = "/* data-theory.js - 理论课堂数据 */\n"
js += "/* P1 Batch1: 5 篇读书报告 x 5 篇 = 25 篇文章已入站 */\n"
js += "/* 待入站: 白皮书(risk-asset) + 投资人五大标准(capital-view) + 岗位认知(career) */\n\n"
js += "SITE_DATA.theory = {\n"
js += "  subsections: " + json.dumps(subsections, ensure_ascii=False, indent=4) + ",\n"
js += "  articles: {\n"

# First, add all new articles (20)
for i, art in enumerate(all_new_articles):
    html = to_html(art.pop("paras"))
    art["contentHtml"] = html
    js += f'    "{art["id"]}": {{\n'
    for key in ["id", "title", "tags", "difficulty", "week", "source", "updated", "section", "subsection", "summary", "relatedIds"]:
        val = json.dumps(art[key], ensure_ascii=False)
        js += f'      "{key}": {val},\n'
    js += f'      "contentHtml": "{html}"\n'
    js += "    },\n"

# Then, extract and re-add 黑天鹅 articles from existing file
# Parse them from the existing JS
black_swan_ids = ["theory-book04-01", "theory-book04-02", "theory-book04-03", "theory-book04-04", "theory-book04-05"]
# Read existing file and extract article blocks
for bs_id in black_swan_ids:
    # Find the article block in existing content
    pattern = f'"{bs_id}":\\s*\\{{([^}}]*(?:\\{{[^}}]*\\}}[^}}]*)*)\\}}'
    match = re_mod.search(pattern, existing_content, re_mod.DOTALL)
    if match:
        # Just copy the block as-is
        block = f'    "{bs_id}": {{{match.group(1)}}}'
        js += block + ",\n"
        print(f"  Preserved: {bs_id}")
    else:
        print(f"  WARNING: Could not find {bs_id} in existing file")

js += "  }\n};\n"

out_path = os.path.join(OUT_DIR, "data-theory.js")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(js)

print(f"\n[OK] data-theory.js updated: {len(all_new_articles) + 5} total articles")
print(f"[OK] File size: {os.path.getsize(out_path) / 1024:.1f} KB")
for a in all_new_articles:
    print(f"  {a['id']}: {a['title'][:40]}...")
