"""
给工具详情页添加 alternatives 反向链接
当工具出现在 alternatives 页面中时，在详情页显示"开源替代品 for XXX"标签
"""
import json, os, re

BASE = os.path.dirname(__file__)
TOOLS_DIR = os.path.join(BASE, 'tools')

# 加载 alternatives 数据
with open(os.path.join(BASE, 'alternatives_data.json'), 'r') as f:
    alt_entries = json.load(f)

# 构建反向映射: tool_id → [(alt_slug, paid_name), ...]
reverse = {}
for entry in alt_entries:
    for aid in entry['alternatives']:
        if aid not in reverse:
            reverse[aid] = []
        reverse[aid].append((entry['slug'], entry['paid_name']))

print(f'反向映射: {len(reverse)} 个工具出现在 alternatives 页面中\n')

# HTML 模板 — 插入在 breadcrumb 之后、Hero 之前
def build_alt_badge(slug, paid_name):
    return f'<a href="../alternatives/{slug}.html" class="alt-ref-badge" title="Open Source {paid_name} Alternative">🔓 {paid_name} Alternative</a>'

STYLE_CSS = """
<style>
.alt-ref-row { display:flex;flex-wrap:wrap;gap:6px;margin:14px 0 0;align-items:center; }
.alt-ref-label { font-size:11px;color:var(--text-3);font-weight:600;text-transform:uppercase;letter-spacing:.05em; }
.alt-ref-badge { display:inline-flex;align-items:center;gap:4px;font-size:11px;font-weight:600;padding:4px 10px;border-radius:999px;background:rgba(52,211,153,.1);border:1px solid rgba(52,211,153,.25);color:#34d399;text-decoration:none;transition:all .15s; }
.alt-ref-badge:hover { background:rgba(52,211,153,.18);border-color:#34d399; }
</style>
"""

updated = 0
skipped = 0

for tool_id, alt_refs in reverse.items():
    path = os.path.join(TOOLS_DIR, f'{tool_id}.html')
    if not os.path.exists(path):
        print(f'  [skip] {tool_id}: 文件不存在')
        skipped += 1
        continue

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查是否已经添加过
    if 'alt-ref-badge' in content:
        print(f'  [skip] {tool_id}: 已有反向链接')
        skipped += 1
        continue

    # 构建 badges HTML
    badges = '\n'.join(build_alt_badge(slug, name) for slug, name in alt_refs[:5])
    alt_html = f'''{STYLE_CSS}
<div class="alt-ref-row">
  <span class="alt-ref-label">Open Source Alternative to:</span>
  {badges}
</div>'''

    # 插入到 breadcrumb 结束 </div> 之后、Hero 之前
    # 匹配: </div>\n\n<!-- Hero -->\n<div class="page-hero"
    # 替换为: </div>\n\n<alt_html>\n<!-- Hero -->\n<div class="page-hero"
    pattern = r'(</div>\s*\n\s*)(<!--\s*Hero)'
    replacement = rf'\1\n{alt_html}\n\2'

    new_content = re.sub(pattern, replacement, content, count=1)

    if new_content == content:
        print(f'  [skip] {tool_id}: 未找到插入位置')
        skipped += 1
        continue

    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f'  [ok] {tool_id}: +{len(alt_refs)} alternatives ({", ".join(n for _,n in alt_refs[:3])}{"..." if len(alt_refs)>3 else ""})')
    updated += 1

print(f'\n完成：更新 {updated} 个工具页，跳过 {skipped} 个')
