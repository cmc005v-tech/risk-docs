# -*- coding: utf-8 -*-
"""接入 checklist 五件套模板到 data-lab.js"""
import sys, os, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

NEW_BASE = r"g:\A工作中心\风险处置Commercial risk management\风险处置学习网站-全量内容md-20260917"
SITE_DIR = r"g:\A工作中心\风险处置Commercial risk management\07_网站源码\risk-learning-site"

def parse_md_file(fpath):
    """Parse markdown file with YAML frontmatter"""
    content = open(fpath, 'r', encoding='utf-8').read()
    
    # Extract frontmatter
    fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
    if not fm_match:
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
                html_lines.append('</table>')
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
        # Table rows
        elif p.startswith('|'):
            if not in_table:
                html_lines.append('<table>')
                in_table = True
            if '---' in p:
                continue
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
    s = s.replace('"', '「').replace('"', '」')
    return s

# ===== Process Checklist Files =====
print("Processing checklist files (沙盘五件套)...")
checklist_files = sorted([f for f in os.listdir(NEW_BASE) if f.startswith('checklist-') and f.endswith('.md')])
checklist_articles = []

for fname in checklist_files:
    fpath = os.path.join(NEW_BASE, fname)
    data = parse_md_file(fpath)
    if data:
        data['section'] = 'lab'
        data['subsection'] = 'checklist'
        data['summary'] = data['summary'].replace('\n', ' ')[:150]
        checklist_articles.append(data)
        print(f"  ✓ {data['id']}: {data['title'][:50]}")

# ===== Read existing data-lab.js and append =====
print(f"\nAppending {len(checklist_articles)} checklist articles to data-lab.js...")
lab_path = os.path.join(SITE_DIR, 'data-lab.js')
lab_content = open(lab_path, 'r', encoding='utf-8').read()

# Add checklist subsection
lab_content = lab_content.replace(
    '{ "id": "lab", "title": "沙盘训练", "status": "active" }',
    '{ "id": "lab", "title": "沙盘训练", "status": "active" },\n    { "id": "checklist", "title": "沙盘五件套模板", "status": "active" }'
)

# Generate new articles JS
new_articles_js = ''
for art in checklist_articles:
    new_articles_js += f'''    "{art['id']}": {{
      "id": "{art['id']}",
      "title": "{escape_js_string(art['title'])}",
      "tags": {art['tags']},
      "difficulty": "{art['difficulty']}",
      "week": "{art['week']}",
      "source": "{escape_js_string(art['source'])}",
      "updated": "{art['updated']}",
      "section": "lab",
      "subsection": "checklist",
      "summary": "{escape_js_string(art['summary'])}",
      "relatedIds": ["lab-01", "lab-02", "lab-03", "lab-04", "lab-05"],
      "contentHtml": "{escape_js_string(art['contentHtml'])}",
      "downloadUrl": ""
    }},
'''

# Find last article and append
lab_content = lab_content.rstrip()
if lab_content.endswith('};'):
    lab_content = lab_content[:-2].rstrip()
    if lab_content.endswith(','):
        lab_content = lab_content[:-1]
    lab_content += ',\n' + new_articles_js.rstrip(',\n') + '\n  }\n};\n'

with open(lab_path, 'w', encoding='utf-8') as f:
    f.write(lab_content)

print(f"✓ data-lab.js: appended {len(checklist_articles)} checklist templates")

# ===== Verify JS syntax =====
print("\nVerifying JS syntax...")
import subprocess
result = subprocess.run(['node', '-c', lab_path], capture_output=True, text=True, encoding='utf-8', errors='replace')
if result.returncode == 0:
    print("  ✓ data-lab.js syntax valid!")
else:
    print(f"  ✗ Syntax error: {result.stderr[:200]}")

print("\n" + "="*60)
print("Checklist 五件套入站完成！")
print(f"  新增: {len(checklist_articles)} 篇模板")
print("  位置: data-lab.js → 沙盘五件套模板子板块")
print("="*60)
