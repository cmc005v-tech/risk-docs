# -*- coding: utf-8 -*-
"""P1 剩余内容批量入站：cases + lab + law + tools + path"""
import sys, os, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

CONTENT_DIR = r"g:\A工作中心\风险处置Commercial risk management\07_网站源码\risk-learning-site\content"
SITE_DIR = r"g:\A工作中心\风险处置Commercial risk management\07_网站源码\risk-learning-site"

def parse_md_file(fname):
    """Parse markdown file with YAML frontmatter"""
    fpath = os.path.join(CONTENT_DIR, fname)
    content = open(fpath, 'r', encoding='utf-8').read()
    
    # Extract frontmatter
    fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
    if not fm_match:
        print(f"  WARNING: No frontmatter in {fname}")
        return None
    
    fm_text = fm_match.group(1)
    body = fm_match.group(2).strip()
    
    # Parse frontmatter fields
    meta = {}
    for line in fm_text.split('\n'):
        if ':' in line:
            key, val = line.split(':', 1)
            meta[key.strip()] = val.strip()
    
    # Convert markdown body to HTML
    html_lines = []
    in_list = False
    in_table = False
    
    for line in body.split('\n'):
        p = line.rstrip()
        if not p:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            if in_table:
                in_table = False
            continue
        
        # Headers
        if p.startswith('## '):
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append(f'<h2>{p[3:]}</h2>')
        elif p.startswith('### '):
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append(f'<h3>{p[4:]}</h3>')
        elif p.startswith('#### '):
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append(f'<h4>{p[5:]}</h4>')
        # List items
        elif p.startswith('- '):
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            html_lines.append(f'<li>{p[2:]}</li>')
        # Table rows (simple handling)
        elif p.startswith('|'):
            if not in_table:
                html_lines.append('<table>')
                in_table = True
            if '---' in p:
                continue  # Skip separator
            cells = [c.strip() for c in p.split('|')[1:-1]]
            html_lines.append('<tr>' + ''.join(f'<td>{c}</td>' for c in cells) + '</tr>')
        else:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            if in_table:
                html_lines.append('</table>')
                in_table = False
            # Bold text
            p = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', p)
            # Links
            p = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', p)
            html_lines.append(f'<p>{p}</p>')
    
    if in_list:
        html_lines.append('</ul>')
    if in_table:
        html_lines.append('</table>')
    
    html = '\n'.join(html_lines)
    
    # Parse tags
    tags_str = meta.get('tags', '[]')
    tags = re.findall(r'[^\[\],]+', tags_str)
    tags = [t.strip() for t in tags if t.strip()]
    
    return {
        'id': meta.get('id', ''),
        'title': meta.get('title', ''),
        'tags': tags,
        'difficulty': meta.get('difficulty', '入门'),
        'week': meta.get('week', 'W0'),
        'source': meta.get('source', ''),
        'updated': meta.get('updated', '2026-09-17'),
        'contentHtml': html,
        'summary': body[:200] if len(body) > 200 else body
    }

def escape_js_string(s):
    """Escape string for JS"""
    s = s.replace('\\', '\\\\')
    s = s.replace('"', '\\"')
    s = s.replace('\n', '\\n')
    s = s.replace('\r', '')
    # Replace Chinese quotes
    s = s.replace('"', '「').replace('"', '」')
    return s

# ===== Process Cases =====
print("Processing cases...")
case_files = sorted([f for f in os.listdir(CONTENT_DIR) if f.startswith('case-') and f.endswith('.md')])
cases_articles = []
for fname in case_files:
    data = parse_md_file(fname)
    if data:
        data['section'] = 'cases'
        data['subsection'] = 'cases'
        data['summary'] = data['summary'].replace('\n', ' ')[:150]
        cases_articles.append(data)
        print(f"  ✓ {data['id']}: {data['title'][:40]}")

# Generate data-cases.js
cases_js = '''/* data-cases.js - 案例库数据 */
/* P1 批次入站：17 个实战案例 */

SITE_DATA.cases = {
  title: "实战案例库",
  subsections: [
    { "id": "cases", "title": "案例库", "status": "active" }
  ],
  articles: {
'''
for art in cases_articles:
    cases_js += f'''    "{art['id']}": {{
      "id": "{art['id']}",
      "title": "{escape_js_string(art['title'])}",
      "tags": {art['tags']},
      "difficulty": "{art['difficulty']}",
      "week": "{art['week']}",
      "source": "{escape_js_string(art['source'])}",
      "updated": "{art['updated']}",
      "section": "cases",
      "subsection": "cases",
      "summary": "{escape_js_string(art['summary'])}",
      "relatedIds": [],
      "contentHtml": "{escape_js_string(art['contentHtml'])}",
      "downloadUrl": ""
    }},
'''
cases_js = cases_js.rstrip(',\n') + '\n  }\n};\n'

with open(os.path.join(SITE_DIR, 'data-cases.js'), 'w', encoding='utf-8') as f:
    f.write(cases_js)
print(f"✓ data-cases.js: {len(cases_articles)} articles\n")

# ===== Process Labs =====
print("Processing labs...")
lab_files = sorted([f for f in os.listdir(CONTENT_DIR) if f.startswith('lab-') and f.endswith('.md')])
lab_articles = []
for fname in lab_files:
    data = parse_md_file(fname)
    if data:
        data['section'] = 'lab'
        data['subsection'] = 'lab'
        data['summary'] = data['summary'].replace('\n', ' ')[:150]
        lab_articles.append(data)
        print(f"  ✓ {data['id']}: {data['title'][:40]}")

# Generate data-lab.js
lab_js = '''/* data-lab.js - 沙盘训练数据 */
/* P1 批次入站：5 个沙盘训练 */

SITE_DATA.lab = {
  title: "沙盘训练",
  subsections: [
    { "id": "lab", "title": "沙盘训练", "status": "active" }
  ],
  articles: {
'''
for art in lab_articles:
    lab_js += f'''    "{art['id']}": {{
      "id": "{art['id']}",
      "title": "{escape_js_string(art['title'])}",
      "tags": {art['tags']},
      "difficulty": "{art['difficulty']}",
      "week": "{art['week']}",
      "source": "{escape_js_string(art['source'])}",
      "updated": "{art['updated']}",
      "section": "lab",
      "subsection": "lab",
      "summary": "{escape_js_string(art['summary'])}",
      "relatedIds": [],
      "contentHtml": "{escape_js_string(art['contentHtml'])}",
      "downloadUrl": ""
    }},
'''
lab_js = lab_js.rstrip(',\n') + '\n  }\n};\n'

with open(os.path.join(SITE_DIR, 'data-lab.js'), 'w', encoding='utf-8') as f:
    f.write(lab_js)
print(f"✓ data-lab.js: {len(lab_articles)} articles\n")

# ===== Process Laws =====
print("Processing laws...")
law_files = sorted([f for f in os.listdir(CONTENT_DIR) if f.startswith('law-') and f.endswith('.md')])
law_articles = []
for fname in law_files:
    data = parse_md_file(fname)
    if data:
        data['section'] = 'law'
        data['subsection'] = 'law'
        data['summary'] = data['summary'].replace('\n', ' ')[:150]
        law_articles.append(data)
        print(f"  ✓ {data['id']}: {data['title'][:40]}")

# Generate data-law.js
law_js = '''/* data-law.js - 法规参考数据 */
/* P1 批次入站：2 个法规要点卡 */

SITE_DATA.law = {
  title: "法规参考",
  subsections: [
    { "id": "law", "title": "法规参考", "status": "active" }
  ],
  articles: {
'''
for art in law_articles:
    law_js += f'''    "{art['id']}": {{
      "id": "{art['id']}",
      "title": "{escape_js_string(art['title'])}",
      "tags": {art['tags']},
      "difficulty": "{art['difficulty']}",
      "week": "{art['week']}",
      "source": "{escape_js_string(art['source'])}",
      "updated": "{art['updated']}",
      "section": "law",
      "subsection": "law",
      "summary": "{escape_js_string(art['summary'])}",
      "relatedIds": [],
      "contentHtml": "{escape_js_string(art['contentHtml'])}",
      "downloadUrl": ""
    }},
'''
law_js = law_js.rstrip(',\n') + '\n  }\n};\n'

with open(os.path.join(SITE_DIR, 'data-law.js'), 'w', encoding='utf-8') as f:
    f.write(law_js)
print(f"✓ data-law.js: {len(law_articles)} articles\n")

# ===== Process Tool Guides (append to data-tools.js) =====
print("Processing tool guides...")
tool_files = sorted([f for f in os.listdir(CONTENT_DIR) if f.startswith('tool-') and f.endswith('.md')])
tool_articles = []
for fname in tool_files:
    data = parse_md_file(fname)
    if data:
        data['section'] = 'tools'
        data['subsection'] = 'tool-guides'
        data['summary'] = data['summary'].replace('\n', ' ')[:150]
        tool_articles.append(data)
        print(f"  ✓ {data['id']}: {data['title'][:40]}")

# Read existing data-tools.js and append new subsection
tools_path = os.path.join(SITE_DIR, 'data-tools.js')
tools_content = open(tools_path, 'r', encoding='utf-8').read()

# Find the closing brace and insert new subsection
# Add tool-guides to subsections
tools_content = tools_content.replace(
    '{ "id": "methods", "title": "方法论卡", "status": "active" }',
    '{ "id": "methods", "title": "方法论卡", "status": "active" },\n    { "id": "tool-guides", "title": "工具指南", "status": "active" }'
)

# Insert new articles before closing brace
new_tools_js = ''
for art in tool_articles:
    new_tools_js += f'''    "{art['id']}": {{
      "id": "{art['id']}",
      "title": "{escape_js_string(art['title'])}",
      "tags": {art['tags']},
      "difficulty": "{art['difficulty']}",
      "week": "{art['week']}",
      "source": "{escape_js_string(art['source'])}",
      "updated": "{art['updated']}",
      "section": "tools",
      "subsection": "tool-guides",
      "summary": "{escape_js_string(art['summary'])}",
      "relatedIds": [],
      "contentHtml": "{escape_js_string(art['contentHtml'])}",
      "downloadUrl": ""
    }},
'''

# Find last article and append
tools_content = tools_content.rstrip()
if tools_content.endswith('};'):
    tools_content = tools_content[:-2].rstrip()
    if tools_content.endswith(','):
        tools_content = tools_content[:-1]
    tools_content += ',\n' + new_tools_js.rstrip(',\n') + '\n  }\n};\n'

with open(tools_path, 'w', encoding='utf-8') as f:
    f.write(tools_content)
print(f"✓ data-tools.js: appended {len(tool_articles)} tool guides\n")

# ===== Process Path (populate 13 weeks) =====
print("Processing path...")
path_file = 'path-01-13周成才路径总览.md'
path_data = parse_md_file(path_file)

# Define 13 weeks structure
weeks_data = {
    'W0': {'title': '启程预备', 'articles': ['career-01'], 'task': '用自己的话写出风险处置顾问和律师、普通风控的3点区别'},
    'W1': {'title': '岗位认知+底色', 'articles': ['career-02'], 'task': '用四步法对一家企业做简易风险排查'},
    'W2': {'title': '尽调筑基I', 'articles': ['tool-06', 'career-03'], 'task': '用尽调清单完成六维信息收集'},
    'W3': {'title': '尽调筑基II+风险定级', 'articles': ['tool-07'], 'task': '用评估表对尽调结果打分定级'},
    'W4': {'title': '理论筑基：风控资产+评估报告', 'articles': ['theory-01', 'tool-02'], 'task': '输出完整风险评估报告'},
    'W5': {'title': '筑基验收', 'articles': ['theory-02'], 'task': '用预判→止损→复盘框架复盘2个案例'},
    'W6': {'title': '稳评+思维模型+资本视角', 'articles': ['theory-03', 'theory-07', 'career-04'], 'task': '完成风险因素清单与评级矩阵'},
    'W7': {'title': '掘金+处置方案书', 'articles': ['theory-04', 'method-01', 'tool-01', 'tool-08'], 'task': '每周1篇完整风险处置方案书'},
    'W8': {'title': '四高频场景×谈判', 'articles': ['method-02', 'tool-05', 'theory-05'], 'task': '用谈判五层心法撰写三段式话术'},
    'W9': {'title': '交易结构+进阶案例', 'articles': ['method-03', 'method-04'], 'task': '设计债转股+引入战投结构方案'},
    'W10': {'title': '隔离止损+舆情+战时五步', 'articles': ['tool-04', 'theory-06', 'method-05'], 'task': '输出隔离止损动作清单+舆情应对三重诊断表'},
    'W11': {'title': '金融谈判沙盘+法规闭环', 'articles': ['lab-01', 'lab-02', 'law-01', 'law-02'], 'task': '完成金融机构谈判推演全部训练任务'},
    'W12': {'title': '爆雷场景全流程实战', 'articles': ['lab-03', 'lab-04', 'lab-05'], 'task': '任选2个场景完成五件套全流程输出'},
    'W13': {'title': '沙盘毕业考+复盘交付', 'articles': ['tool-03'], 'task': '综合沙盘考核+输出结案复盘报告'}
}

# Read existing data-path.js and update
path_js_path = os.path.join(SITE_DIR, 'data-path.js')
path_content = open(path_js_path, 'r', encoding='utf-8').read()

# Replace empty weeks object with populated data
weeks_js = '  weeks: {\n'
for week_id, wdata in weeks_data.items():
    weeks_js += f'    "{week_id}": {{\n'
    weeks_js += f'      "title": "{wdata["title"]}",\n'
    weeks_js += f'      "articles": {wdata["articles"]},\n'
    weeks_js += f'      "task": "{wdata["task"]}"\n'
    weeks_js += f'    }},\n'
weeks_js = weeks_js.rstrip(',\n') + '\n  },\n'

# Replace weeks: {} with populated weeks
path_content = re.sub(r'  weeks: \{\},', weeks_js, path_content)

# Add path-01 article
if path_data:
    path_article_js = f'''  articles: {{
    "path-overview": {{
      "id": "path-overview",
      "title": "13 周成才路径总览",
      "tags": ["入门", "W0-W13", "学习路径"],
      "difficulty": "入门",
      "week": "W0-W13",
      "source": "风险处置学习方案 2026-09",
      "updated": "2026-09-17",
      "section": "path",
      "subsection": "overview",
      "summary": "13周系统学习路径：筑基期（W0-W5）→进阶期（W6-W9）→成型期（W10-W13）。每周含目标、必读文章、实操作业与验收标准。",
      "relatedIds": [],
      "contentHtml": "{escape_js_string(path_data['contentHtml'])}",
      "downloadUrl": ""
    }}
  }}'''
    path_content = re.sub(r'  articles: \{[^}]*\}', path_article_js, path_content, flags=re.DOTALL)

with open(path_js_path, 'w', encoding='utf-8') as f:
    f.write(path_content)
print(f"✓ data-path.js: populated 14 weeks (W0-W13) + path-overview article\n")

print("="*60)
print("P1 剩余内容入站完成！")
print(f"  案例库: {len(cases_articles)} 篇")
print(f"  沙盘训练: {len(lab_articles)} 篇")
print(f"  法规参考: {len(law_articles)} 篇")
print(f"  工具指南: {len(tool_articles)} 篇")
print(f"  学习路径: 14 周数据 + 1 篇总览")
print("="*60)
