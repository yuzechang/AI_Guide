#!/usr/bin/env python3
"""
批量修复：
1. 所有博客文章中的 "AI Nav Editorial Team" → "Nolan" + 作者页链接
2. 首页 meta keywords 删除中文关键词
3. about.html：更新 Nolan 的实际背景信息

运行：python3 patch_author_and_meta.py
"""

import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BLOG_DIR = os.path.join(BASE_DIR, "blog")

# ──────────────────────────────────────────────
# 1. 批量修复博客作者署名
# ──────────────────────────────────────────────

OLD_AUTHOR_SPAN = '✍️ AI Nav Editorial Team'
NEW_AUTHOR_SPAN = '✍️ <a href="/authors/nolan" style="color:inherit;text-decoration:underline;text-underline-offset:3px">Nolan</a>'

OLD_AUTHOR_SCHEMA = '"name": "AI Nav Editorial Team"'
NEW_AUTHOR_SCHEMA_BLOG = '''"name": "Nolan",
      "alternateName": "yuzc",
      "url": "https://yuzec.com/authors/nolan",
      "sameAs": ["https://github.com/yuzechang", "https://x.com/ZechangYu"]'''

changed_blogs = 0
for fname in sorted(os.listdir(BLOG_DIR)):
    if not fname.endswith(".html") or fname == "index.html":
        continue
    fpath = os.path.join(BLOG_DIR, fname)
    with open(fpath, encoding="utf-8") as f:
        html = f.read()

    new_html = html
    # 替换显示署名
    new_html = new_html.replace(OLD_AUTHOR_SPAN, NEW_AUTHOR_SPAN)
    # 替换 Schema author name
    new_html = re.sub(
        r'"name":\s*"AI Nav Editorial Team"',
        NEW_AUTHOR_SCHEMA_BLOG,
        new_html
    )
    # 删除旧的 "url": "https://yuzec.com/" author url（避免重复）
    new_html = re.sub(
        r',\s*"url":\s*"https://yuzec\.com/"(\s*,\s*"sameAs":\s*\["https://github\.com/yuzechang"\])?',
        '',
        new_html
    )
    if new_html != html:
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(new_html)
        changed_blogs += 1
        print(f"  [OK] blog/{fname}")

print(f"\n已修复博客署名: {changed_blogs} 个文件")

# ──────────────────────────────────────────────
# 2. 首页 meta keywords 删除中文词
# ──────────────────────────────────────────────

INDEX_PATH = os.path.join(BASE_DIR, "index.html")
with open(INDEX_PATH, encoding="utf-8") as f:
    html = f.read()

# 删除中文关键词（逗号分隔）
new_html = re.sub(
    r'(content="[^"]*),AI工具导航,AI工具大全,智能体框架,AI工具推荐2026',
    r'\1',
    html
)
if new_html != html:
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(new_html)
    print("\n[OK] index.html meta keywords 已删除中文关键词")
else:
    print("\n[SKIP] index.html keywords 未找到中文词（可能已修改）")

# ──────────────────────────────────────────────
# 3. about.html 更新 Nolan 背景信息
# ──────────────────────────────────────────────

ABOUT_PATH = os.path.join(BASE_DIR, "about.html")
with open(ABOUT_PATH, encoding="utf-8") as f:
    html = f.read()

new_html = html

# 更新职位描述
new_html = new_html.replace(
    'Software Engineer · AI Tools Practitioner',
    'Test Engineer · AI Tools Practitioner'
)

# 更新背景卡片
new_html = new_html.replace(
    '<div class="info-card-value" style="font-size:16px">AI Engineering</div>\n        <div class="info-card-sub">AI application development, developer tooling, ML infrastructure</div>',
    '<div class="info-card-value" style="font-size:16px">Software Testing</div>\n        <div class="info-card-sub">Test automation, script writing, QA tooling, AI-assisted development</div>'
)

# 修复 about.html 里的 "software engineer" 描述
new_html = new_html.replace(
    'AI Nav is built and maintained by <strong>Nolan (yuzc)</strong>, a software engineer working with AI tools professionally.',
    'AI Nav is built and maintained by <strong>Nolan (yuzc)</strong>, a test engineer who uses AI tools in daily work — writing automation scripts, building websites, and debugging production issues.'
)

# 添加 X 链接到 GitHub 旁边（在 GitHub 卡片后插入 X 卡片）
OLD_ABOUT_CONTACT = '''      <div class="info-card">
        <div class="info-card-label">✉️ Contact</div>'''
NEW_ABOUT_CONTACT = '''      <div class="info-card">
        <div class="info-card-label">🐦 X / Twitter</div>
        <div class="info-card-value" style="font-size:16px"><a href="https://x.com/ZechangYu" target="_blank" rel="noopener" style="color:var(--accent)">@ZechangYu</a></div>
        <div class="info-card-sub">AI tools, open source, dev notes</div>
      </div>
      <div class="info-card">
        <div class="info-card-label">✉️ Contact</div>'''

if OLD_ABOUT_CONTACT in new_html and '@ZechangYu' not in new_html:
    new_html = new_html.replace(OLD_ABOUT_CONTACT, NEW_ABOUT_CONTACT)

# 修改 "Deployment or integration test" 说法为更诚实的表述
new_html = new_html.replace(
    '<li><strong>Deployment or integration test</strong> — For tools with &gt;5,000 stars, we deploy or run the tool locally to verify the quickstart experience matches what\'s advertised.</li>',
    '<li><strong>Hands-on assessment</strong> — Where possible, tools are run locally or via Docker to check that the quickstart experience matches what the documentation claims. Notes from these tests show up in the tool\'s Getting Started and Expert Take sections.</li>'
)

if new_html != html:
    with open(ABOUT_PATH, "w", encoding="utf-8") as f:
        f.write(new_html)
    print("[OK] about.html 已更新背景信息")
else:
    print("[SKIP] about.html 未发生变化")

print("\n完成。")
