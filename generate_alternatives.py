"""
为每个付费工具生成 /alternatives/{slug}.html 页面
从 alternatives_data.json 读取配置，从 data.json 拉取工具详情
"""
import json, os
from jinja2 import Environment, FileSystemLoader

BASE = os.path.dirname(__file__)
ALT_DIR = os.path.join(BASE, 'alternatives')
TEMPLATES_DIR = os.path.join(BASE, 'templates')

# 确保输出目录存在
os.makedirs(ALT_DIR, exist_ok=True)

# 加载数据
with open(os.path.join(BASE, 'data.json'), 'r') as f:
    data = json.load(f)
tools = {t['id']: t for t in data['tools']}

with open(os.path.join(BASE, 'alternatives_data.json'), 'r') as f:
    alt_entries = json.load(f)

# 设置 Jinja2
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

# 确保 header.html 和 footer.html 存在
header_path = os.path.join(TEMPLATES_DIR, 'header.html')
footer_path = os.path.join(TEMPLATES_DIR, 'footer.html')
for p, name in [(header_path, 'header.html'), (footer_path, 'footer.html')]:
    if not os.path.exists(p):
        print(f'[warn] {name} 不存在，创建空白模板')
        with open(p, 'w') as f:
            f.write('')

def render_alt(entry):
    """渲染单个 alternatives 页面"""
    slug = entry['slug']
    paid_name = entry['paid_name']

    # 收集替代工具详情
    alt_alternatives = []
    for aid in entry['alternatives']:
        if aid in tools:
            t = tools[aid]
            alt_alternatives.append(t)
        else:
            print(f'  [warn] 工具 {aid} 在 data.json 中不存在，已跳过')

    if not alt_alternatives:
        print(f'  [skip] {slug}: 没有可用的替代工具')
        return False

    # 按 stars 排序
    alt_alternatives.sort(key=lambda x: x.get('stars', 0), reverse=True)

    # SEO 标题：含关键词 + 具体价值
    seo_title = f"Best Open Source {paid_name} Alternatives in 2026 — Free & Self-Hosted | AI Nav"

    # SEO 描述：列出前 3 个工具名
    top3 = [t['name'] for t in alt_alternatives[:3]]
    seo_desc = (
        f"Looking for a free {paid_name} alternative? "
        f"Compare the best open source options: {', '.join(top3)}. "
        f"Self-hosted, private, and no subscription fees."
    )

    html = env.get_template('alternatives.j2').render(
        seo_title=seo_title,
        seo_desc=seo_desc,
        base_url='https://yuzec.com',
        alt=entry,
        alt_alternatives=alt_alternatives,
    )

    output_path = os.path.join(ALT_DIR, f'{slug}.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    return True

# 执行生成
updated = 0
skipped = 0

print(f'共 {len(alt_entries)} 个 alternatives 页面待生成\n')

for entry in alt_entries:
    if render_alt(entry):
        print(f'  [ok] alternatives/{entry["slug"]}.html ({entry["paid_name"]})')
        updated += 1
    else:
        skipped += 1

print(f'\n完成：生成 {updated} 个页面，跳过 {skipped} 个')
print(f'输出目录: {ALT_DIR}')
