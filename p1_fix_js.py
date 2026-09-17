# -*- coding: utf-8 -*-
"""Fix JS syntax errors in data-tools.js and data-path.js"""
import sys, os, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

SITE_DIR = r"g:\A工作中心\风险处置Commercial risk management\07_网站源码\risk-learning-site"

# ===== Fix data-tools.js =====
print("Fixing data-tools.js...")
tools_path = os.path.join(SITE_DIR, 'data-tools.js')
content = open(tools_path, 'r', encoding='utf-8').read()

# The issue: articles object was closed prematurely, new articles are outside it
# Pattern: ...last original article}\n  },\n    "tool-01": {
# Fix: remove the premature closing of articles
# Find the pattern: "}\n  },\n    \"tool-01\":" and replace with "},\n    \"tool-01\":"
content = content.replace(
    '    }\n  },\n    "tool-01":',
    '    },\n    "tool-01":'
)

with open(tools_path, 'w', encoding='utf-8') as f:
    f.write(content)

# Verify
try:
    import subprocess
    result = subprocess.run(['node', '-c', tools_path], capture_output=True, text=True)
    if result.returncode == 0:
        print("  ✓ data-tools.js syntax valid!")
    else:
        print(f"  ✗ Still has error: {result.stderr[:200]}")
except:
    print("  (node check skipped)")

# ===== Fix data-path.js =====
print("\nFixing data-path.js...")
path_path = os.path.join(SITE_DIR, 'data-path.js')
content = open(path_path, 'r', encoding='utf-8').read()

# The issue: contentHtml for path-overview has literal newlines
# Need to find the contentHtml value and escape all newlines within it
# Strategy: find "contentHtml": "..." pattern and replace internal newlines

def fix_content_html(match):
    prefix = match.group(1)  # "contentHtml": "
    body = match.group(2)    # the HTML content with literal newlines
    suffix = match.group(3)  # closing quote + comma or not
    
    # Replace literal newlines with \n
    body = body.replace('\r\n', '\\n').replace('\n', '\\n').replace('\r', '')
    
    return prefix + body + suffix

# Find the path-overview contentHtml - it starts after "relatedIds": [],
# and spans multiple lines until the closing "
# Use a regex that matches "contentHtml": "..."..." where ... can span lines
# The content ends at a line that has ",\n or "\n

lines = content.split('\n')
fixed_lines = []
in_content_html = False
html_buffer = []

for i, line in enumerate(lines):
    if '"contentHtml":' in line and not line.strip().endswith('",'):
        # This line starts a multi-line contentHtml
        in_content_html = True
        html_buffer = [line]
        continue
    elif in_content_html:
        html_buffer.append(line)
        if line.strip().endswith('",') or line.strip().endswith('"'):
            # End of multi-line contentHtml
            in_content_html = False
            # Join all lines and escape newlines
            full = '\n'.join(html_buffer)
            # Extract the contentHtml value
            m = re.match(r'(\s*"contentHtml":\s*")(.*)(",?\s*)$', full, re.DOTALL)
            if m:
                prefix = m.group(1)
                body = m.group(2)
                suffix = m.group(3)
                # Escape newlines in body
                body = body.replace('\n', '\\n').replace('\r', '')
                fixed_lines.append(prefix + body + suffix)
            else:
                fixed_lines.extend(html_buffer)
            html_buffer = []
        continue
    else:
        fixed_lines.append(line)

content = '\n'.join(fixed_lines)

with open(path_path, 'w', encoding='utf-8') as f:
    f.write(content)

# Verify
try:
    result = subprocess.run(['node', '-c', path_path], capture_output=True, text=True)
    if result.returncode == 0:
        print("  ✓ data-path.js syntax valid!")
    else:
        print(f"  ✗ Still has error: {result.stderr[:200]}")
except:
    print("  (node check skipped)")

print("\nDone!")
